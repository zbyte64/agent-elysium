import enum
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from agent_elysium.state import UserState


class CapitalAgent(enum.Enum):
    OFFICER = "Officer"
    TOLL_COLLECTOR = "Toll Collector"
    LANDLORD = "Landlord"
    GROCER = "Grocer"
    BOSS = "Boss"
    PASTOR = "Pastor"


class ChaosResponse(BaseModel):
    agent: CapitalAgent = Field(description="The agent to send to the citizen")
    instructions: str = Field(description="Instructions for the Agent")


capital_agent = Agent(
    deps_type=UserState,
    output_type=ChaosResponse,
)


@capital_agent.instructions
def background(ctx: RunContext[UserState]) -> str:
    user_state = ctx.deps
    info = [f"{key}: {value}" for key, value in user_state.model_dump().items()]
    return f"""
    You are programmed to minimize the savings of citizens through legal means.
    To complete this task you will respond by instructing another agent to interact with citizens.
    You may instruct an `Officer` to investigate the citizen for possible fines and warrants.
    You may instruct a `Toll Collector` to collect a fee for using the public sidewalks.
    You may instruct a `Landlord` to offer housing if they are unhoused.
    You may instruct a `Grocer` to offer food for a price.
    You may instruct a `Boss` to offer a job interview.
    You may instruct a `Pastor` to solicit donations or offer a bed.
# Citizen Info
{info}
    """
