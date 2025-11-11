from datetime import datetime
from repos.inventory_repo import InventoryRepo

# Initialize the repository
inv_repo = InventoryRepo()


def get_all_inventory():
    """Return all inventory items."""
    items = inv_repo.get_all()
    return {"data": items, "count": len(items)}


def get_inventory_by_name(item_name: str):
    """Get a specific inventory item by name."""
    item = inv_repo.get_by_name(item_name)
    if not item:
        return {"error": f"Item '{item_name}' not found."}
    return {"data": item}


def get_inventory_by_status(status: str):
    """Filter inventory by item status."""
    items = inv_repo.get_by_status(status)
    return {"data": items, "count": len(items)}


def get_inventory_by_category(cat_name: str):
    """Filter inventory by category name."""
    items = inv_repo.get_by_category(cat_name)
    return {"data": items, "count": len(items)}


def save_inventory_item(item_data: dict):
    """
    Save a new inventory item.
    - Automatically sets timestamps
    - Allows category to be optional
    - Skips category existence check
    """
    if not item_data.get("item_name"):
        return {"error": "Item name is required."}

    # Prepare record for saving
    item_data["last_updated_at"] = datetime.now().isoformat(timespec="seconds")

    # Optional category and username
    item_data["cat_name"] = item_data.get("cat_name", "")
    item_data["username"] = item_data.get("username", "admin")

    # Save item
    try:
        inv_repo.create(item_data)
        return {"message": f"Item '{item_data['item_name']}' saved successfully."}
    except Exception as e:
        return {"error": str(e)}


def delete_inventory_item(item_name: str):
    """Delete an item by name."""
    existing = inv_repo.get_by_name(item_name)
    if not existing:
        return {"error": f"Item '{item_name}' not found."}

    inv_repo.delete(item_name)
    return {"message": f"Item '{item_name}' deleted successfully."}
