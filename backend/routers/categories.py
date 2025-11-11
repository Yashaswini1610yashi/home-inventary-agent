from fastapi import APIRouter
from services import category_service
from models.data_models import Category

router = APIRouter()

@router.get("/")
def get_all_categories():
    return category_service.get_all_categories()

@router.post("/")
def save_category(category: Category):
    return category_service.save_category(category)

@router.delete("/{cat_name}")
def delete_category(cat_name: str):
    return category_service.delete_category(cat_name)
