from fastapi import APIRouter
from services import user_service
from utils import *

router = APIRouter()

@router.get("/")
def get_all_users():
    return user_service.get_all_users()

@router.get("/{username}")
def get_user(username: str):
    return user_service.get_user_by_username(username)

@router.post("/")
def save_user(user: dict):
    return user_service.save_user(user)

@router.delete("/{username}")
def delete_user(username: str):
    return user_service.delete_user(username)
