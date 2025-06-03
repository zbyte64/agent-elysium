import enum
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from agent_elysium.state import UserState
from faker import Faker

fake = Faker()


class Scene(enum.Enum):
    CHURCH = "Church"
    # PARK = 'Park'
    FLAT = "Flat"
    JOB = "Job"
    SIDEWALK = "Sidewalk"


class NextScene(BaseModel):
    place: Scene = Field(default=Scene.SIDEWALK)


dungeon_master_agent = Agent(
    deps_type=UserState,
    instructions="""
Simulate a dungeon master. Take the user response and translate their intent into a scene.
""",
    output_type=NextScene,
)
