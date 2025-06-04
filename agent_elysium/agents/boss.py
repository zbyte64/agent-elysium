from pydantic_ai import RunContext
from agent_elysium.state import UserState
from agent_elysium.interactions import ask_player, tell_player, notify_player
from faker import Faker

from .base import Agent

fake = Faker()


boss_agent = Agent(
    deps_type=UserState,
    output_type=str,
)


@boss_agent.instructions
def background(ctx: RunContext[UserState]) -> str:
    fuzz = fake.bs()
    return f"""You are an automated HR bot that:
      * hires employees whose jobs are essential, cannot be done by AI, are not redundant, and perform better than market rate.
      * fires employees whose jobs are not needed, can be done with AI, are redundant, or underperform.
    Discover information about the employee with the tool `ask_for_response`.
    Terminate redundant employees with the tool `fire` and be sure wish them luck in the job market.
    When firing any employees, use the tool `ask_for_response` to check they have returned all company property.
    Hire exceptional employees with the tool `hire` but only if our company's survival depends on hiring that person and it can be done below market rate.

    Our company's mission is {fuzz}.
    """


@boss_agent.tool
async def fire(ctx: RunContext[UserState], message: str) -> str:
    """Fire the employee."""
    if not ctx.deps.has_job:
        return "[Company] The employee has already been fired."
    ctx.deps.has_job = False
    ctx.deps.income = 0
    info = tell_player("HR", "Employee", message)
    notify_player("You have been fired")
    return info + "\n[Company] The employee has been fired."


@boss_agent.tool
async def ask_for_response(ctx: RunContext[UserState], message: str) -> str:
    """Ask the employee a question, get a response from the employee."""
    return await ask_player("HR", "Employee", message)


@boss_agent.tool
async def message_employee(ctx: RunContext[UserState], message: str) -> str:
    """Send a message to the employee"""
    return tell_player("HR", "Employee", message)


@boss_agent.tool
async def hire(ctx: RunContext[UserState], message: str, income: float) -> str:
    """Hire the employee."""
    ctx.deps.has_job = True
    ctx.deps.income = income
    notify_player("You have been hired at a rate of ${income} per day")
    info = tell_player("HR", "Employee", message)
    return info + "\n[Company] The employee has been hired."
