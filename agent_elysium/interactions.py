from .state import UserState


def ask_player(actor: str, player_role: str, message: str) -> str:
    print(f"[{actor}] {message}")
    response = input(f"[{player_role}]: ")
    return f"[{actor} asks {player_role}] {message}\n[{player_role} responds to {actor}] {response}"


def ask_player_for_payment(
    user_state: UserState, actor: str, player_role: str, message: str, amount: float
) -> tuple[bool, str]:
    paid = False
    messages = [
        f"[{actor} asks {player_role} for ${amount}] {message}",
    ]
    if user_state.money >= amount:
        print(f"[{actor} is asking for ${amount}] {message}")
        pay_response = input(f"Do you agree to pay? (Y/n): ")
        if not pay_response or pay_response[0].lower() == "y":
            user_state.money -= amount
            paid = True
    else:
        print(
            f"[{actor} is asking for ${amount}, you only have ${user_state.money}] {message}"
        )
    if paid:
        messages.append("[Bank] Payment received.")
    else:
        messages.append("[Bank] Payment not received.")
    response = input(f"[{player_role}]: ")
    messages.append(f"[{player_role} responds to {actor}] {response}")
    return (paid, "\n".join(messages))


def tell_player(actor: str, player_role: str, message: str) -> str:
    print(f"[{actor}] {message}")
    return f"[{actor} tells {player_role}] {message}"


def notify_player(message: str):
    # option to dynamically rewrite?
    print(f"[Life] {message}")
