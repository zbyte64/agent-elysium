import logging

from agent_elysium.state import UserState
from agent_elysium.agents.pastor import pastor_agent
from agent_elysium.interactions import notify_player


async def arrive(user_state: UserState):
    if user_state.rent_paid:
        user_state.rent_paid = (user_state.day % 5) != 0
    notify_player("You arrive at the shelter. You goto sleep.")
    if user_state.rent_paid:
        notify_player("You wakeup at the shelter. You see the pastor approach.")
        result = await pastor_agent.run(
            "The citizen needs to be encouraged to find work by evicting them from their bed.",
            deps=user_state,
        )
        logging.info(result.output)
    else:
        notify_player("You wakeup at the shelter.")
