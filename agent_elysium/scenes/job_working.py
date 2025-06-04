from agent_elysium.agents.boss import boss_agent
from agent_elysium.state import UserState
from agent_elysium.interactions import notify_player


async def arrive(user_state: UserState):
    if user_state.has_job:
        user_state.money += user_state.income
        notify_player(
            f"You arrive at your job. ${user_state.income} was automatically deposited into your bank. The friendly HR avatar appears on your work computer."
        )
        await boss_agent.run(
            "Please fire the employee as their job has been automated with AI. Be sure to verify they have returned all company property before they are fired.",
            deps=user_state,
        )
    else:
        # TODO robot?
        notify_player(
            f"You arrive at the job center. A friendly HR avatar appears in front of you."
        )
        boss_agent.run(
            "Please evaluate the perspective employee for hire. Ensure they align with our business and our strategic AI efforts. Do not hire them if their tasks can be performed by AI. After the interview inform the employee of your decision and it's basis.",
            deps=user_state,
        )
