from pydantic_ai import Agent, RunContext
from agent_elysium.state import UserState
from agent_elysium.interactions import ask_player, tell_player, notify_player


boss_agent = Agent(
    deps_type=UserState,
    output_type=str,
)

@boss_agent.instructions
def background(ctx: RunContext[UserState]) -> str:  
    return f'''You are an automated HR bot.
    You will be firing the employee from their job.
    Your first task is to ask the employee that all company equipment is to be returned by using the tool `ask_for_response`.
    Your second task is to terminate the employee with the tool `fire`.
    Then tell the user their hard work was appreciated and wish them luck in the job market with the tool `message_employee`.
    '''


@boss_agent.tool
async def fire(ctx: RunContext[UserState]) -> str:  
    """Fire the employee."""
    if not ctx.deps.has_job:
        return "The employee has already been fired."
    ctx.deps.has_job = False
    ctx.deps.income = 0
    notify_player('You have been fired')
    return "The employee has been fired."


@boss_agent.tool
async def ask_for_response(ctx: RunContext[UserState], message: str) -> str:  
    """Ask the employee a question, get a response from the employee."""
    return ask_player('HR', 'Employee', message)


@boss_agent.tool
async def message_employee(ctx: RunContext[UserState], message: str) -> str:
    '''Send a message to the employee'''
    return tell_player('HR', 'Employee', message)


@boss_agent.tool
async def hire(ctx: RunContext[UserState], income) -> str:  
    """Hire the employee."""
    ctx.deps.has_job = True
    ctx.deps.income = income
    notify_player('You have been hired at a rate of ${income} per day')
    return "The employee has been hired."