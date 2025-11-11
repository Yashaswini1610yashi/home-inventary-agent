from fastapi import APIRouter
from services import inventory_service
from models.data_models import Inventory

router = APIRouter()

@router.get("/")
def get_all_inventory():
    return inventory_service.get_all_inventory()

@router.get("/name/{item_name}")
def get_inventory_by_name(item_name: str):
    return inventory_service.get_inventory_by_name(item_name)

@router.get("/status/{status}")
def get_inventory_by_status(status: str):
    return inventory_service.get_inventory_by_status(status)

@router.get("/category/{cat_name}")
def get_inventory_by_category(cat_name: str):
    return inventory_service.get_inventory_by_category(cat_name)

@router.post("/")
def save_inventory_item(item: dict):
    return inventory_service.save_inventory_item(item)

@router.delete("/{item_name}")
def delete_inventory_item(item_name: str):
    return inventory_service.delete_inventory_item(item_name)
