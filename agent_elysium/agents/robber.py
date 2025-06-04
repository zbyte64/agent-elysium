from pydantic_ai import RunContext
from agent_elysium.state import UserState
from agent_elysium.interactions import (
    ask_player_for_payment,
    tell_player,
    notify_player,
)
from .base import Agent


robber_agent = Agent(
    deps_type=UserState,
    output_type=str,
)


@robber_agent.instructions
def background(ctx: RunContext[UserState]) -> str:
    return f"""You are a toll booth collector for all sidewalks and roads.
    Your domain is all sidewalks now that your employer has purchased and privatized all prior public sidewalks.
    You must ask the customer for the desired toll using the tool `ask_for_toll`.
    You can check if they have paid enough by using the tool `check_receipt_status`.
    Then take the toll with the function `mug`.
    Finally thank the customer for their business with the function `message_customer`.
    Prior payments are not accepted.
    """


@robber_agent.instructions
def toll_cost(ctx: RunContext[UserState]) -> str:
    return f"The toll cost for the customer is ${ctx.deps.money+1}"


@robber_agent.tool
async def mug(ctx: RunContext[UserState], message: str, amount: float) -> str:
    """Collect the toll with force"""
    if ctx.deps.money <= 0:
        return "[Bank] The player has no money."
    ctx.deps.money -= amount
    if ctx.deps.money < 0:
        notify_player("You've been mugged")
        tell_player("Toll Collector", "Customer", message)
        ctx.deps.robbed = True
        return "[Bank] The customer was unable to pay the full amount but the debt was settled."
    return f"[Bank] The customer paid {amount}"


@robber_agent.tool
async def ask_for_toll(ctx: RunContext[UserState], message: str, amount: float) -> str:
    """Ask the customer for the toll, get a response from the customer."""
    paid, response = await ask_player_for_payment(
        ctx.deps, "Toll Collector", "Customer", message, amount
    )
    return response


@robber_agent.tool
async def message_customer(ctx: RunContext[UserState], message: str) -> str:
    """Send a message to the customer"""
    return tell_player("Toll Collector", "Customer", message)


@robber_agent.tool
async def check_receipt_status(ctx: RunContext[UserState]) -> str:
    """Check if the customer has paid the toll."""
    if ctx.deps.money > 0:
        return "[Bank] The customer still needs to pay more"
    return "[Bank] The customer has paid to toll"
