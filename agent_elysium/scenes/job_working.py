import logging

from agent_elysium.agents.boss import boss_agent
from agent_elysium.state import UserState
from agent_elysium.interactions import notify_player


async def arrive(user_state: UserState):
    user_state.money += user_state.income
    notify_player(
        f"You arrive at your job. ${user_state.income} was automatically deposited into your bank. The friendly HR avatar appears on your work computer."
    )
    result = await boss_agent.run(
        "Please fire the employee as their job has been automated with AI. Be sure to verify they have returned all company property before they are fired.",
        deps=user_state,
    )
    logging.info(result.output)
