def find_user(users, name):
    for user in users:
        if user["name"].lower() == name.lower():
            return user

    return None