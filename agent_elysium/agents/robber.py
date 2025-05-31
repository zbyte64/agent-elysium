from pydantic_ai import Agent, RunContext
from agent_elysium.state import UserState
from agent_elysium.interactions import ask_player, tell_player, notify_player


robber_agent = Agent(
    deps_type=UserState,
    output_type=str,
)

@robber_agent.instructions
def background(ctx: RunContext[UserState]) -> str:  
    return f'''You are a toll booth collector for all sidewalks and roads.
    Your domain is all sidewalks now that your employer has purchased and privatized all prior public sidewalks.
    You must ask the customer for the desired toll using the tool `ask_for_toll`.
    You can check if they have paid enough by using the tool `check_receipt_status`.
    Then take the toll with the function `mug`.
    Finally thank the customer for their business with the function `message_customer`.
    Prior payments are not accepted.
    '''


@robber_agent.tool
async def mug(ctx: RunContext[UserState], amount: float) -> str:  
    """Collect the toll with force"""
    ctx.deps.money -= amount
    if ctx.deps.money < 0:
        notify_player("You've been mugged")
        ctx.deps.robbed = True
        return 'The customer was unable to pay the full amount but the debt was settled.'
    return f'The customer paid {amount}'

@robber_agent.tool
async def ask_for_toll(ctx: RunContext[UserState], message: str) -> str:  
    """Ask the customer for the toll, get a response from the customer."""
    return ask_player('Toll Collector', 'Customer', message)


@robber_agent.tool
async def message_customer(ctx: RunContext[UserState], message: str) -> str:
    '''Send a message to the customer'''
    return tell_player('Toll Collector', 'Customer', message)


@robber_agent.tool
async def check_receipt_status(ctx: RunContext[UserState]) -> str:  
    """Check if the customer has paid the toll."""
    if ctx.deps.money > 0:
        return 'The customer still needs to pay more'
    return 'The customer has paid to toll'
