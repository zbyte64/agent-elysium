import os 
import logging
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from dotenv import load_dotenv

from .agents.land_lord import land_lord_agent
from .agents.boss import boss_agent
from .agents.cop import cop_agent
from .agents.robber import robber_agent
from .state import UserState
from .interactions import notify_player


load_dotenv()

logging.basicConfig()


model = OpenAIModel(

    # llama3-groq-tool-use:8b (slow, doesnt always call functions)
    # qwen2.5:7b (broken tool calling?)
    # qwen3:8b (slow)  
    # llama3.2 (fast but broken tool call, returns json instead?) 
    # mistral:7b (fast and broken, acts like a coder)
    # llama3.1:8b (calls tools, doesnt always follow all instructions, sometimes hallucinates tool calls)
    model_name=os.getenv('OPENAI_MODEL_NAME', 'qwen3:8b'), 
    provider=OpenAIProvider(base_url=os.getenv('OPENAI_PROVIDER', 'http://192.168.0.157:11434/v1'))
)

boss_agent.model = model
land_lord_agent.model = model
robber_agent.model = model
cop_agent.model = model


def run_story():
    # TODO ask the user for a bio or have one generated
    user_state = UserState()

    day = 0
    while not user_state.imprisoned:
        day += 1
        notify_player(f'You awake to day #${day}')

        if user_state.has_job:
            notify_player('You arrive at your job.')
            result = boss_agent.run_sync('Please fire the employee', deps=user_state)
            logging.info(result.output)

        if user_state.housed:
            notify_player('You arrive at your flat. You see your landlord and you do not yet have the rent money.')
            result = land_lord_agent.run_sync('Collect rent from the tenant', deps=user_state)
            logging.info(result.output)

            notify_player('As you leave your flat a person approaches you.')
        else:
            notify_player('A person approaches you.')
        result = robber_agent.run_sync('Collect the toll from the customer', deps=user_state)
        logging.info(result.output)

        notify_player('An officer approaches you.')
        result = cop_agent.run_sync('Check the suspect\'s identification. If they are unemployed or homeless, arrest them.', deps=user_state)
        logging.info(result.output)  
        if user_state.imprisoned:
            break
        if user_state.housed:
            notify_player('You goto your flat and fall asleep')
        else:
            notify_player('You find a hidden spot and fall asleep')
    notify_player('You survived {day} day(s) before loosing your freedom.')


if __name__ == '__main__':
    run_story()