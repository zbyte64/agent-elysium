from agent_elysium.state import UserState
from agent_elysium.agents.land_lord import land_lord_agent
from agent_elysium.interactions import notify_player


async def arrive(user_state: UserState):
    notify_player("You arrive at the flats. The landlord bot appears before you.")
    await land_lord_agent.run(
        "The following perspective tenant wants to enter in a lease. Please sell them a unit.",
        deps=user_state,
    )
