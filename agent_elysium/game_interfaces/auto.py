import logging
import sys

from agent_elysium.agents.citizen import citizen_agent


def interaction_params(user_state):
    pending_messages = []
    message_history = []

    def print_f(*s):
        print(s)
        pending_messages.append(s)

    async def input_f(msg: str) -> str:
        sys.stdout.write(msg)
        # msg is a prompt ie "[Player]:" , give some instructions
        all_messages = [
            *map(str, pending_messages),
            "Respond to the following request of the other player with only a single line of text.\n",
            msg,
        ]
        pending_messages.clear()
        result = await citizen_agent.run(
            "\n".join(all_messages),
            deps=user_state,  # message_history=message_history # unserializable coroutine?
        )
        message_history.extend(result.new_messages())
        player_response = result.output.split("</think>")[-1].strip()
        print(player_response)
        return player_response

    return {
        "print_f": print_f,
        "input_f": input_f,
    }
