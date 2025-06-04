from agent_elysium.interactions import PLAYER_INTERACTION
from agent_elysium.agents.dungeon_master import dungeon_master_agent, Scene
from .scenes import sidewalk_traveling, church, job_working, flat_seeking
from .interactions import ExitScene, notify_player


SCENE_MAPPING = {
    # Scene.PARK: '',
    Scene.CHURCH: church,
    Scene.JOB: job_working,
    Scene.FLAT: flat_seeking,
}


async def arrive(user_state):
    leaving = user_state.leaving
    # ask user for destination
    response = await PLAYER_INTERACTION.ask_player(
        "DM", "Player", "Where do you want to go?"
    )
    result = await dungeon_master_agent.run(response, deps=user_state)
    desired_scene = result.output
    place = desired_scene.place
    notify_player(f"You start traveling the sidewalk towards {place.value}")

    # walk to the destination
    try:
        await sidewalk_traveling.arrive(user_state, leaving)
    except ExitScene as e:
        notify_player(e.args[0])

    dest = SCENE_MAPPING.get(place, None)
    if dest:
        user_state.leaving = place.value
        await dest.arrive(user_state)
