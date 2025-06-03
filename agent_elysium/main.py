import asyncio
import os
import logging
from pydantic_ai.settings import ModelSettings
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from dotenv import load_dotenv

from . import agents, scenes, user_traveling
from .state import UserState
from .interactions import notify_player, PLAYER_INTERACTION
from .game_interfaces import auto


load_dotenv()

logging.basicConfig(level=logging.INFO)


model = OpenAIModel(
    # llama3-groq-tool-use:8b (slow, doesnt always call functions)
    # qwen2.5:7b (broken tool calling?)
    # qwen3:8b (slow)
    # llama3.2 (fast but broken tool call, returns json instead?)
    # mistral:7b (fast and broken, acts like a coder)
    # llama3.1:8b (calls tools, doesnt always follow all instructions, sometimes hallucinates tool calls)
    model_name=os.getenv("OPENAI_MODEL_NAME", "qwen3:8b"),
    provider=OpenAIProvider(
        base_url=os.getenv("OPENAI_PROVIDER", "http://127.0.0.1:11434/v1")
    ),
)


for agent_name in dir(agents):
    if not agent_name.endswith("_agent"):
        continue
    agent = getattr(agents, agent_name)
    agent.model = model
    agent.model_settings = ModelSettings(timeout=int(os.getenv("API_TIMEOUT", 300)))


def run_story_with_params(user_state: UserState):
    return asyncio.run(async_run_story_with_params(user_state))


async def async_run_story_with_params(user_state: UserState):
    while not user_state.imprisoned:
        user_state.day += 1
        leaving = None
        if user_state.housed:
            if user_state.rent_cost:
                await scenes.flat_sleeping.arrive(user_state=user_state)
                leaving = "flat"
            else:
                await scenes.shelter_sleeping.arrive(user_state=user_state)
                leaving = "shelter"
        else:
            await scenes.sidewalk_sleeping.arrive(user_state=user_state)
            leaving = "sidewalk"

        if user_state.has_job:
            await scenes.job_working.arrive(user_state)
            leaving = "job"

        # ask user for destination
        await user_traveling.arrive(user_state, leaving)

    notify_player(f"You survived {user_state.day} day(s) before loosing your freedom.")


def run_story():
    # TODO ask the user for a bio or have one generated
    user_state = UserState()
    run_story_with_params(user_state)


def run_auto_story():
    user_state = UserState()
    logging.info("Using citizen bot to simulate gameplay")
    PLAYER_INTERACTION.set_interface(**auto.interaction_params(user_state=user_state))
    run_story_with_params(user_state)


if __name__ == "__main__":
    run_story()
