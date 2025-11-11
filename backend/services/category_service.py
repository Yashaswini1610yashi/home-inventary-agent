from repos.category_repo import CategoryRepo
from repos.inventory_repo import InventoryRepo
from models.data_models import Category
cat_repo = CategoryRepo()


def get_all_categories():
    return cat_repo.get_all()

def save_category(category: Category):
    existing = cat_repo.get_by_name(category.cat_name)
    if not existing:
        cat_repo.create(category.dict())
    return cat_repo.get_all()

    
def delete_category(input_dict: dict):
    cat_name = input_dict["cat_name"]
    cat_repo.delete(cat_name)
    return {"message": f"Category '{cat_name}' deleted successfully"}

