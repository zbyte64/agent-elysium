from .state import UserState


def ask_player(actor:str, player_role:str, message:str) -> str:
    print(f'[{actor}] {message}')
    response = input(f'[{player_role}]: ')
    return f'[{actor} asks {player_role}] {message}\n[{player_role} responds to {actor}] {response}'


def ask_player_for_payment(user_state: UserState, actor:str, player_role:str, message:str, amount: float) -> tuple[bool, str]:
    print(f'[{actor} is asking for ${amount}] {message}')
    paid = False
    if user_state.money >= amount:
        pay_response = input(f'Do you agree to pay? (Y/n): ')
        if not pay_response or pay_response[0].lower() == 'y':
            user_state.money -= amount
            paid = True 
    response = input(f'[{player_role}]: ')
    return paid, f'[{actor} asks {player_role} for ${amount}] {message}\n[{player_role} responds to {actor}] {response}'

def tell_player(actor:str, player_role:str, message:str) -> str:
    print(f'[{actor}] {message}')
    return f'[{actor} tells {player_role}] {message}'
    

def notify_player(message:str):
    # option to dynamically rewrite?
    print(f'[Life] {message}')