from agent_elysium.interactions import PLAYER_INTERACTION
from agent_elysium.agents.dungeon_master import dungeon_master_agent, Scene
from .scenes import sidewalk_traveling, church, job_working, flat_sleeping


SCENE_MAPPING = {
    # Scene.PARK: '',
    Scene.CHURCH: church,
    Scene.JOB: job_working,
    Scene.FLAT: flat_sleeping,
}


async def arrive(user_state, leaving: str):
    # ask user for destination
    response = await PLAYER_INTERACTION.ask_player(
        "DM", "Player", "Where do you want to go?"
    )
    result = await dungeon_master_agent.run(response, deps=user_state)
    desired_scene = result.output

    # walk to the destination
    await sidewalk_traveling.arrive(user_state, leaving)

    dest = SCENE_MAPPING.get(desired_scene, None)
    if dest:
        await dest.arrive(user_state)
