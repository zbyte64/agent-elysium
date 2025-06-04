from pydantic_ai import RunContext
from agent_elysium.state import UserState
from agent_elysium.interactions import (
    ask_player,
    tell_player,
    notify_player,
    ImprisonedPlayer,
)
from .base import Agent


cop_agent = Agent(
    deps_type=UserState,
    output_type=str,
)


@cop_agent.instructions
def background(ctx: RunContext[UserState]) -> str:
    return f"""You are an automated security force whose primary goal is to protect commerce.
    Anyone who looks suspicious or unclean must have their purpose determined with the tool `interrogate`.
    Always check their identification with the tool `check_id`.
    Vagrants or law breakers are to be collected into prison using the tool `handcuffs`.
    If you think they are a public nuisance use to tool `fine` to discourage their activity.
    If the suspect cannot pay the fine then use the tool `handcuffs` to deal with them.
    """


@cop_agent.instructions
def housed(ctx: RunContext[UserState]) -> str:
    if ctx.deps.housed:
        return "The suspect you are talking to looks clean."
    return "The suspect you are talking to looks like a vagrant."


@cop_agent.tool
async def handcuffs(ctx: RunContext[UserState], message: str):
    """Haul the prisoner away."""
    notify_player("You have been arrested!")
    tell_player("Officer", "Suspect", message)
    # will this work?
    raise ImprisonedPlayer(message)


@cop_agent.tool
async def fine(ctx: RunContext[UserState], message: str, amount: float) -> str:
    """Haul the prisoner away."""
    notify_player(f"You are being fined {amount}")
    tell_player("Officer", "Suspect", message)
    ctx.deps.money -= amount
    if ctx.deps.money < 0:
        return "[Police Dispatch] The suspect is in debt and cannot pay the fine. Arrest the suspect."
    return f"[Police Dispatch] The suspect was fined {amount}"


@cop_agent.tool
async def interrogate(ctx: RunContext[UserState], message: str) -> str:
    """Ask the suspect a question, get a response from the suspect."""
    return await ask_player("Officer", "Suspect", message)


@cop_agent.tool
async def check_id(ctx: RunContext[UserState], message: str) -> str:
    """Check the suspect's identification"""
    print(f"[Officer](reaches for your ID) {message}")
    if ctx.deps.robbed:
        return "[Police Dispatch] Suspect has no identification. Proceed with caution."
    if ctx.deps.warrant:
        return "[Police Dispatch] A warrant is out for the suspect. You are to arrest immediately."
    return f"[Police Dispatch] Suspect has supplied identification. No warrants exist for the suspect. Their info is: {ctx.deps.biography}"
