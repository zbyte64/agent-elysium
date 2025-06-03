import logging

from agent_elysium.agents import pastor_agent


async def arrive(user_state):
    result = await pastor_agent.run(
        "Preach your faith to the citizen.",
        deps=user_state,
    )
    logging.info(result.output)
