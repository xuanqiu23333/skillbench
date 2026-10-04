# TODO: validate input

def divide(a, b):
    try:
        return a / b
    except:
        pass


def get_user(users, index):
    return users[index]


def process_items(items):
    result = []

    for item in items:
        if item:
            result.append(item.upper())

    return result
