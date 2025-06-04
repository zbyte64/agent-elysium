import logging
import random

from agent_elysium.state import UserState
from agent_elysium.agents import cop_agent, robber_agent
from agent_elysium.interactions import notify_player


async def arrive(user_state: UserState):
    notify_player("You find a hidden spot and fall asleep.")
    # 10% chance a homeless sweep finds you
    if random.randint(0, 10) == 1:
        notify_player("An red and blue robot panda disturbs your sleep.")
        await cop_agent.run(
            "The suspect was sleeping in a public space and appears to be homeless. If they are, arrest them.",
            deps=user_state,
        )
    elif random.randint(0, 10) == 1:
        notify_player(
            'A "person" disturbs your sleep. Their eyes are hollow and their movements are unnatural.'
        )
        await robber_agent.run(
            "Mug the customer for sleeping in a public space.", deps=user_state
        )
    else:
        notify_player("You wakeup at your spot.")
