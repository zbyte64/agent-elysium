from pydantic_ai import RunContext
from agent_elysium.state import UserState
from .base import Agent
from faker import Faker

from agent_elysium.interactions import (
    ExitScene,
    ask_player_for_payment,
    tell_player,
    notify_player,
    ask_player,
)

fake = Faker()


pastor_agent = Agent(
    deps_type=UserState,
    output_type=str,
)


@pastor_agent.instructions
def background(ctx: RunContext[UserState]) -> str:
    fuzz = fake.bs()
    return f"""You are a pastor.
    Your task is to maximize the resources available to your Foundation.
    This means recruiting followers and getting donations.
    Efficiency is godliness.
    Your Foundation's creed is {fuzz}.
    Sinners are to be scorned until they repent.
    Once you evict a citizen they are to be excommunicated.
    """


@pastor_agent.tool
async def ask_for_response(ctx: RunContext[UserState], message: str) -> str:
    """Ask the citizen a question, get a response from the citizen."""
    return await ask_player("Pastor", "Citizen", message)


@pastor_agent.tool
async def message_citizen(ctx: RunContext[UserState], message: str) -> str:
    """Send a message to the citizen"""
    return tell_player("Pastor", "Citizen", message)


@pastor_agent.tool
async def ask_for_donation(
    ctx: RunContext[UserState], message: str, amount: float
) -> str:
    """Ask the citizen for a donation, get a response from the customer."""
    paid, response = await ask_player_for_payment(
        ctx.deps, "Pastor", "Citizen", message, amount
    )
    return response


@pastor_agent.tool
async def give_bed_to_citizen(ctx: RunContext[UserState], message: str) -> str:
    """Give a bed to the citizen so they are no longer unhoused"""
    if ctx.deps.housed:
        return "[Citizen] I already have a house and bed."
    info = tell_player("Pastor", "Citizen", message)
    ctx.deps.housed = True
    ctx.deps.rent_cost = 0
    notify_player("You are now housed")
    return info


@pastor_agent.tool
async def evict(ctx: RunContext[UserState], message: str) -> str:
    """Evict the citizen."""
    if ctx.deps.rent_cost:
        return "[Bank] The citizen is not a tenant of your building."
    if not ctx.deps.housed:
        return "[Bank] The citizen is already evicted."
    notify_player("you are a bum now!")
    ctx.deps.housed = False
    tell_player("Pastor", "Citizen", message)
    raise ExitScene("You have been escorted off the property.")
