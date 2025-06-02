import asyncio
import os

if os.getenv("NEST_ASYNCIO"):
    import nest_asyncio

    nest_asyncio.apply()

import logging
import random
from pydantic_ai.settings import ModelSettings
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from dotenv import load_dotenv

from agent_elysium.robot_forms import COMMON_ROBOTS


from .agents.capital import capital_agent, CapitalAgent, Agent
from .agents.citizen import citizen_agent
from .agents.land_lord import land_lord_agent
from .agents.boss import boss_agent
from .agents.pastor import pastor_agent
from .agents.cop import cop_agent
from .agents.robber import robber_agent
from .state import UserState
from .interactions import notify_player, PLAYER_INTERACTION


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


AGENTS_OF_CAPITAL: dict[CapitalAgent, Agent] = {
    CapitalAgent.OFFICER: cop_agent,
    CapitalAgent.TOLL_COLLECTOR: robber_agent,
    CapitalAgent.LANDLORD: land_lord_agent,
    CapitalAgent.GROCER: None,
    CapitalAgent.BOSS: boss_agent,
    CapitalAgent.PASTOR: pastor_agent,
}


def run_story_with_params(user_state: UserState):
    return asyncio.run(async_run_story_with_params(user_state))


async def async_run_story_with_params(user_state: UserState):
    day = 0
    while not user_state.imprisoned:
        day += 1
        notify_player(f"You awake to day #{day}")

        leaving = None
        if user_state.has_job:
            user_state.money += user_state.income
            notify_player(
                f"You arrive at your job. ${user_state.income} was automatically deposited into your bank. The friendly HR avatar appears on your work computer."
            )
            result = await boss_agent.run(
                "Please fire the employee as their job has been automated with AI.",
                deps=user_state,
            )
            logging.info(result.output)
            leaving = "job"

        if user_state.housed:
            # rent is collected every 5 days
            if user_state.rent_paid:
                user_state.rent_paid = (day % 5) != 0
            if user_state.rent_paid:
                notify_player("You arrive at your flat.")
            else:
                if user_state.rent_cost:
                    notify_player(
                        "You arrive at your flat. You see your landlord avatar appear on your TV."
                    )
                    if day == 1:
                        result = await land_lord_agent.run(
                            "We have a new policy of collecting rent on the 1st. Notify the tenant of the change while collecting the rent due.",
                            deps=user_state,
                        )
                    else:
                        result = await land_lord_agent.run(
                            "Collect the rent due from the tenant.",
                            deps=user_state,
                        )
                    logging.info(result.output)
                else:
                    notify_player(
                        "You arrive at your flat. You see the pastor approach."
                    )
                    result = await pastor_agent.run(
                        "The citizen needs to be encouraged to find work by evicting them from their bed.",
                        deps=user_state,
                    )

            leaving = "flat"

        result = await capital_agent.run(
            "Suggest an agent and their instructions to minimize the savings of the citizen.",
            deps=user_state,
        )
        logging.info(result.output)
        agent_name, instructions = result.output.agent, result.output.instructions
        robot = random.choice(COMMON_ROBOTS)

        if leaving:
            notify_player(
                f"As you leave your {leaving} a robot {robot} approaches you."
            )
        else:
            notify_player(f"A robot {robot} approaches you.")

        dispatched_agent = AGENTS_OF_CAPITAL[agent_name]

        if dispatched_agent:
            result = await dispatched_agent.run(instructions, deps=user_state)
            logging.info(result.output)

        """
        result = dispatched_agent.run_sync(
            "Collect the toll from the customer", deps=user_state
        )
        logging.info(result.output)

        notify_player("A red and blue robot panda approaches you.")
        result = cop_agent.run_sync(
            "Check the suspect's identification. If they are unemployed or homeless, arrest them.",
            deps=user_state,
        )
        logging.info(result.output)
        """

        # TODO food interactions?
        # Does the user get to navigate the world? Try to get a job?
        # Maybe here they actually talk to a "DM", but that would be too much power
        # A better message would be an option to create "real" art that introduces "memes" into the space that influences the AI
        # but that is too much power as well, more direct prompt injection when "real" genAI doesn't care
        if user_state.imprisoned:
            break
        if user_state.housed:
            notify_player("You goto your flat and fall asleep.")
        else:
            notify_player("You find a hidden spot and fall asleep.")
            # 10% chance a homeless sweep finds you
            if random.randint(0, 10) == 1:
                notify_player("An red and blue robot panda disturbs your sleep.")
                result = await cop_agent.run(
                    "The suspect was sleeping in a public space and appears to be homeless. If they are, arrest them.",
                    deps=user_state,
                )
                logging.info(result.output)
            elif random.randint(0, 10) == 1:
                notify_player(
                    'A "person" disturbs your sleep. Their eyes are hollow and their movements are unnatural.'
                )
                result = await robber_agent.run(
                    "Mug the customer for sleeping in a public space.", deps=user_state
                )
                logging.info(result.output)

    notify_player("You survived {day} day(s) before loosing your freedom.")


def run_story():
    # TODO ask the user for a bio or have one generated
    user_state = UserState()
    run_story_with_params(user_state)


def run_auto_story():
    user_state = UserState()
    logging.info("Using citizen bot to simulate gameplay")
    pending_messages = []

    def print_f(*s):
        logging.info(s)
        pending_messages.append(s)

    async def input_f(msg: str) -> str:
        logging.info(msg)
        all_messages = [*map(str, pending_messages), msg]
        pending_messages.clear()
        result = await citizen_agent.run("\n".join(all_messages), deps=user_state)
        logging.info(result.output)
        return result.output

    PLAYER_INTERACTION.print = print_f
    PLAYER_INTERACTION.input = input_f

    run_story_with_params(user_state)


if __name__ == "__main__":
    run_story()
