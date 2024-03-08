from random import choice, randint

def get_response(user_input: str):
    lowered = user_input.lower()

    if lowered == '':
        return 'you are not saying nothing'
    elif 'hello' in lowered:
        return 'hello there'
    else:
        return choice(['idk', 'nah id win'])