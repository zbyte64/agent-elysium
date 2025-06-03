import logging

from agent_elysium.state import UserState
from agent_elysium.agents.land_lord import land_lord_agent
from agent_elysium.interactions import notify_player


async def arrive(user_state: UserState):
    # rent is collected every 5 days
    if user_state.rent_paid:
        user_state.rent_paid = (user_state.day % 5) != 0
    notify_player("You arrive at your flat. You goto sleep.")
    if user_state.rent_paid:
        notify_player("You wakeup at your flat.")
    else:
        notify_player(
            "You wakeup at your flat. You see your landlord avatar appear on your TV."
        )
        if user_state.day == 1:
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
