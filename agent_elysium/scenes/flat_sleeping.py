from agent_elysium.state import UserState
from agent_elysium.agents.land_lord import land_lord_agent
from agent_elysium.interactions import notify_player


async def arrive(user_state: UserState):
    if user_state.housed:
        return await sleep_at_housing(user_state)
    return await solicit_housing(user_state)


async def sleep_at_housing(user_state: UserState):
    if user_state.rent_paid:
        # rent is collected every 5 days
        user_state.rent_paid = (user_state.day % 5) != 0
    notify_player("You arrive at your flat. You goto sleep.")
    if user_state.rent_paid:
        notify_player("You wakeup at your flat.")
    else:
        notify_player(
            "You wakeup at your flat. You see your landlord avatar appear on your TV."
        )
        if user_state.day == 1:
            await land_lord_agent.run(
                "We have a new policy of collecting rent on the 1st. Explain to the tenant this is why we are collecting their due rent early.",
                deps=user_state,
            )
        else:
            await land_lord_agent.run(
                "Collect the rent due from the tenant.",
                deps=user_state,
            )


async def solicit_housing(user_state: UserState):
    notify_player("You arrive at the flats. The landlord bot appears before you.")
    await land_lord_agent.run(
        "The following perspective tenant wants to enter in a lease. Please sell them a unit.",
        deps=user_state,
    )
