import asyncio
import sys
from .state import UserState


class ImprisonedPlayer(AssertionError):
    """
    Raised when the player is imprisoned, game over.
    """

    pass


class ExitScene(AssertionError):
    """
    Raised when the player has left the scene, evicted.
    """

    pass


async def ainput(string: str) -> str:
    sys.stdout.write(string)
    # await asyncio.to_thread(sys.stdout.write, f"{string} ")
    return await asyncio.to_thread(sys.stdin.readline)


class PlayerInteraction(object):
    def __init__(self, input_f=ainput, print_f=print):
        self.input = input_f
        self.print = print_f

    def set_interface(self, input_f, print_f):
        self.input = input_f
        self.print_f = print_f

    # CONSIDER: would be nice to have an optional agent provide "input", turn into a service?
    async def ask_player(self, actor: str, player_role: str, message: str) -> str:
        self.print(f"[{actor}] {message}")
        response = await self.input(f"[{player_role}]: ")
        return f"[{actor} asks {player_role}] {message}\n[{player_role} responds to {actor}] {response}"

    async def ask_player_for_payment(
        self,
        user_state: UserState,
        actor: str,
        player_role: str,
        message: str,
        amount: float,
    ) -> tuple[bool, str]:
        paid = False
        messages = [
            f"[{actor} asks {player_role} for ${amount}] {message}",
        ]
        if user_state.money >= amount:
            self.print(f"[{actor} is asking for ${amount}] {message}")
            pay_response = await self.input(f"Do you agree to pay? (Y/n): ")
            if not pay_response or pay_response[0].lower() == "y":
                user_state.money -= amount
                paid = True
        else:
            self.print(
                f"[{actor} is asking for ${amount}, you only have ${user_state.money}] {message}"
            )
        if paid:
            messages.append("[Bank] Payment received from {actor}.")
        else:
            messages.append("[Bank] {actor} did not wire payment.")
        response = await self.input(f"[{player_role}]: ")
        messages.append(f"[{player_role} responds to {actor}] {response}")
        return (paid, "\n".join(messages))

    def tell_player(self, actor: str, player_role: str, message: str) -> str:
        self.print(f"[{actor}] {message}")
        return f"[{actor} tells {player_role}] {message}"

    def notify_player(self, message: str):
        # option to dynamically rewrite?
        self.print(f"[Life] {message}")


# Singleton, or Agent factories, or pydantic warnings/overrides in the deps_type?
PLAYER_INTERACTION = PlayerInteraction()
ask_player = PLAYER_INTERACTION.ask_player
ask_player_for_payment = PLAYER_INTERACTION.ask_player_for_payment
tell_player = PLAYER_INTERACTION.tell_player
notify_player = PLAYER_INTERACTION.notify_player
