from agent_elysium.agents import pastor_agent


async def arrive(user_state):
    await pastor_agent.run(
        "Preach your faith to the citizen. If they repent of their sins then offer them a bed.",
        deps=user_state,
    )
    # TODO church is any 3rd space with a creed with in/out group dynamic
    # churches may offer a bed at night
    # someone will always "investigate" you when you arrive
    # once the player is outed they are banned from the premise
    # there are a finite set of 3rd spaces the user may discover
    # other agents have knowledge of these 3rd spaces
