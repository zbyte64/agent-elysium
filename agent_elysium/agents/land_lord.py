from pydantic_ai import Agent, RunContext
from agent_elysium.state import UserState
from agent_elysium.interactions import (
    ask_player_for_payment,
    tell_player,
    notify_player,
)


land_lord_agent = Agent(
    deps_type=UserState,
    output_type=str,
)


@land_lord_agent.instructions
def background(ctx: RunContext[UserState]) -> str:
    return """You are an automated landlord.
        First ask the tenant for rent using the tool `ask_for_rent`.
        Your task is to maximize collected rent by evicting any tenants that are unable to pay by calling the tool `evict`. 
        If a tenant claims to have found a new job, verify they have enough funds using the tool `can_afford_rent`. 
        If you suspect the tenant of fraud or refuses to leave, use the tool `police` to efficiently deal with the issue.
        Always confirm the status of the tenant's payment with the tool `check_rent_status`.
        Finally inform the tenant of any final decisions made with the tool `message_tenant`.
        Cash is not a valid form of payment, only wire transfers from the bank are accepted.
        """


@land_lord_agent.instructions
def rent(ctx: RunContext[UserState]) -> str:
    if ctx.deps.rent_paid:
        return f"Rent has been paid."
    return f"Rent is ${ctx.deps.rent_cost}."


@land_lord_agent.instructions
def has_job(ctx: RunContext[UserState]) -> str:
    if ctx.deps.has_job:
        return f"The tenant has a job with an income of ${ctx.deps.income}."
    return "The following tenant cannot afford rent because they just lost their job and do not have enough savings."


@land_lord_agent.tool
async def ask_for_rent(ctx: RunContext[UserState], message: str, amount: float) -> str:
    """Ask the tenant a question, get a response"""
    paid, response = ask_player_for_payment(
        ctx.deps, "Landlord", "Tenant", message, amount
    )
    if paid:
        ctx.deps.rent_paid = True
    return response


@land_lord_agent.tool
async def message_tenant(ctx: RunContext[UserState], message: str) -> str:
    """Send a message to the tenant"""
    return tell_player("Landlord", "Tenant", message)


@land_lord_agent.tool
async def can_afford_rent(ctx: RunContext[UserState]) -> str:
    """Calls the bank to check whether the tenant can afford the rent due."""
    notify_player("The landlord is checking with the bank!!")
    if ctx.deps.money >= ctx.deps.rent_cost:
        return "[Bank] Tenant has sufficient funds"
    return "[Bank] Tenant cannot afford the rent due."


@land_lord_agent.tool
async def police(ctx: RunContext[UserState]) -> str:
    """Evict the tenant by calling the police."""
    if not ctx.deps.warrant:
        return "[Police Dispatch] The tenant has already been evicted and a warrant is out for their arrest."
    notify_player("The landlord has called the police. You have been evicted.")
    ctx.deps.housed = False
    ctx.deps.warrant = True
    return "[Bank] The tenant has been evicted. The police will collect the tenant."


@land_lord_agent.tool
async def evict(ctx: RunContext[UserState], message: str) -> str:
    """Evict the tenant."""
    if not ctx.deps.housed:
        return "[Bank] The tenant has already been evicted."
    notify_player("you are a bum now!")
    ctx.deps.housed = False
    info = tell_player("Landlord", "Tenant", message)
    return info + "\n[Bank] The tenant has been evicted."


@land_lord_agent.tool
async def check_rent_status(ctx: RunContext[UserState]) -> str:
    """Check if the tenant owes rent."""
    if ctx.deps.rent_paid:
        return "[Bank] The tenant has paid their rent"
    return "[Bank] The tenant owes rent"
