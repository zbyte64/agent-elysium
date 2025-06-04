import logging
import random

from pydantic_ai import Agent

from agent_elysium.agents.capital import CapitalAgent
from agent_elysium.robot_forms import COMMON_ROBOTS
from agent_elysium.state import UserState
from agent_elysium.agents import capital_agent
from agent_elysium import agents
from agent_elysium.interactions import notify_player


AGENTS_OF_CAPITAL: dict[CapitalAgent, tuple[Agent, str]] = {
    CapitalAgent.OFFICER: (
        agents.cop_agent,
        "Check the suspect's identification. If they are unemployed or homeless, arrest them.",
    ),
    CapitalAgent.TOLL_COLLECTOR: (
        agents.robber_agent,
        "Collect the toll from the customer",
    ),
    # CapitalAgent.LANDLORD: agents.land_lord_agent,
    # CapitalAgent.GROCER: None,
    # CapitalAgent.BOSS: agents.boss_agent,
    CapitalAgent.PASTOR: (agents.pastor_agent, "Preach your faith to the citizen."),
}


async def arrive(user_state: UserState, leaving: str):
    if user_state.day > 10:
        result = await capital_agent.run(
            "Suggest an agent and their instructions to minimize the savings of the citizen.",
            deps=user_state,
        )
        agent_name, instructions = result.output.agent, result.output.instructions
        robot = random.choice(COMMON_ROBOTS)

        if leaving:
            notify_player(
                f"As you leave your {leaving} a robot {robot} approaches you."
            )
        else:
            notify_player(f"A robot {robot} approaches you.")

        dispatched_agent, default_prompt = AGENTS_OF_CAPITAL[agent_name]

        if dispatched_agent:
            result = await dispatched_agent.run(instructions, deps=user_state)
    else:
        agent_name, (dispatched_agent, default_prompt) = random.choice(
            list(AGENTS_OF_CAPITAL.items())
        )

        match agent_name:
            case CapitalAgent.OFFICER:
                notify_player("A red and blue robot panda approaches you.")
            case _:
                robot = random.choice(COMMON_ROBOTS)
                notify_player(f"A robot {robot} approaches you.")

        result = await dispatched_agent.run(default_prompt, deps=user_state)
