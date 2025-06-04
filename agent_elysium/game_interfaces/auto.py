import logging
import sys

from agent_elysium.agents.citizen import citizen_agent


def interaction_params(user_state):
    pending_messages = []

    # TODO preserve chat history

    def print_f(*s):
        print(s)
        pending_messages.append(s)

    async def input_f(msg: str) -> str:
        sys.stdout.write(msg)
        all_messages = [*map(str, pending_messages), msg]
        pending_messages.clear()
        result = await citizen_agent.run("\n".join(all_messages), deps=user_state)
        print(result.output)
        return result.output

    return {
        "print_f": print_f,
        "input_f": input_f,
    }
