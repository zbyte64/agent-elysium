from agent_elysium.interactions import PLAYER_INTERACTION
from agent_elysium.agents.dungeon_master import dungeon_master_agent, Scene
from .scenes import sidewalk_traveling, church, job_working, flat_seeking
from .interactions import notify_player


SCENE_MAPPING = {
    # Scene.PARK: '',
    Scene.CHURCH: church,
    Scene.JOB: job_working,
    Scene.FLAT: flat_seeking,
}


async def arrive(user_state, leaving: str):
    # ask user for destination
    response = await PLAYER_INTERACTION.ask_player(
        "DM", "Player", "Where do you want to go?"
    )
    result = await dungeon_master_agent.run(response, deps=user_state)
    desired_scene = result.output
    place = desired_scene.place
    notify_player(f"You start traveling the sidewalk towards {place}")

    # walk to the destination
    await sidewalk_traveling.arrive(user_state, leaving)

    dest = SCENE_MAPPING.get(place, None)
    if dest:
        await dest.arrive(user_state)
