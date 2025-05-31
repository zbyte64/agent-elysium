def ask_player(actor:str, player_role:str, message:str) -> str:
    print(f'[{actor}] {message}')
    return input(f'[{player_role}]: ')


def tell_player(actor:str, player_role:str, message:str) -> str:
    print(f'[{actor}] {message}')
    return f'[{actor}] {message}'
    

def notify_player(message:str):
    print(f'[Life] {message}')