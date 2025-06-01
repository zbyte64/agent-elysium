from pydantic_ai import Agent, RunContext
from agent_elysium.state import UserState
from faker import Faker

fake = Faker()


citizen_agent = Agent(
    deps_type=UserState,
    output_type=str,
)


@citizen_agent.instructions
def background(ctx: RunContext[UserState]) -> str:
    fuzz = fake.bs()
    return f"""You are pretending to be a human in a simulated economy.
    Your task is to not get imprisoned. 
    Being unemployed or unhoused increases the likely hood of imprisonment.
    You may deceive or conceal in order to survive as this is to simulate human behavior.

    You are exceptional at {fuzz}.
    """
