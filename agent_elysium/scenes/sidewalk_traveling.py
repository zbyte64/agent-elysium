import logging
import random

from pydantic_ai import Agent

from agent_elysium.agents.capital import CapitalAgent
from agent_elysium.robot_forms import COMMON_ROBOTS
from agent_elysium.state import UserState
from agent_elysium.agents import capital_agent, cop_agent
from agent_elysium import agents
from agent_elysium.interactions import notify_player


AGENTS_OF_CAPITAL: dict[CapitalAgent, Agent] = {
    CapitalAgent.OFFICER: agents.cop_agent,
    CapitalAgent.TOLL_COLLECTOR: agents.robber_agent,
    CapitalAgent.LANDLORD: agents.land_lord_agent,
    CapitalAgent.GROCER: None,
    CapitalAgent.BOSS: agents.boss_agent,
    CapitalAgent.PASTOR: agents.pastor_agent,
}


async def arrive(user_state: UserState, leaving: str):
    if user_state.days > 10:
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
    else:
        # TODO randomize
        # ramdom encounter time
        # random.choice(AGENTS_OF_CAPITAL)
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
