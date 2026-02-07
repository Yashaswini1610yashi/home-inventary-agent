from repos.user_repo import UserRepo
user_repo = UserRepo()


def get_all_users():
    return user_repo.get_all()

def get_user_by_username(username: str):
    return user_repo.get_by_username(username)

def save_user(user_data: dict):
    existing = user_repo.get_by_username(user_data["username"])
    if existing:
        user_repo.update(user_data["username"], user_data)
    else:
        user_repo.create(user_data)
    return user_repo.get_by_username(user_data["username"])

def delete_user(username: str):
    user_repo.delete(username)
    return {"message": "User deleted successfully"}

