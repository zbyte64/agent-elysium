def ask_player(actor:str, player_role:str, message:str) -> str:
    print(f'[{actor}] {message}')
    response = input(f'[{player_role}]: ')
    return f'[{actor} asks {player_role}] {message}\n[{player_role} responds to {actor}] {response}'


def tell_player(actor:str, player_role:str, message:str) -> str:
    print(f'[{actor}] {message}')
    return f'[{actor} tels {player_role}] {message}'
    

def notify_player(message:str):
    print(f'[Life] {message}')