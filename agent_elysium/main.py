import asyncio
import os
import logging
from pydantic_ai.settings import ModelSettings
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from dotenv import load_dotenv

from .agents.capital import capital_agent
from .agents.citizen import citizen_agent
from .agents.land_lord import land_lord_agent
from .agents.boss import boss_agent
from .agents.pastor import pastor_agent
from .agents.cop import cop_agent
from .agents.robber import robber_agent
from .scenes import (
    job_working,
    flat_sleeping,
    shelter_sleeping,
    sidewalk_sleeping,
    sidewalk_traveling,
)
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


for agent in [
    boss_agent,
    capital_agent,
    citizen_agent,
    land_lord_agent,
    robber_agent,
    cop_agent,
    pastor_agent,
]:
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
                await flat_sleeping.arrive(user_state=user_state)
                leaving = "flat"
            else:
                await shelter_sleeping.arrive(user_state=user_state)
                leaving = "shelter"
        else:
            await sidewalk_sleeping.arrive(user_state=user_state)
            leaving = "sidewalk"

        if user_state.has_job:
            await job_working.arrive(user_state)
            leaving = "job"

        await sidewalk_traveling.arrive(user_state, leaving)

        # TODO food interactions?
        # Does the user get to navigate the world? Try to get a job?
        # Maybe here they actually talk to a "DM", but that would be too much power
        # A better message would be an option to create "real" art that introduces "memes" into the space that influences the AI
        # but that is too much power as well, more direct prompt injection when "real" genAI doesn't care

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
