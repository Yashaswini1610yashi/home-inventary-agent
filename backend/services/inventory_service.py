# services/inventory_service.py
from datetime import datetime, timedelta
from repos.inventory_repo import InventoryRepo

# Initialize repository
inv_repo = InventoryRepo()


def get_all_inventory():
    items = inv_repo.get_all()
    return {"data": items, "count": len(items) if items is not None else 0}


def get_inventory_by_name(item_name: str):
    item = inv_repo.get_by_name(item_name)
    if not item:
        return {"error": f"Item '{item_name}' not found."}
    return {"data": item}


def get_inventory_by_status(status: str):
    items = inv_repo.get_by_status(status)
    return {"data": items, "count": len(items) if items is not None else 0}


def get_inventory_by_category(cat_name: str):
    items = inv_repo.get_by_category(cat_name)
    return {"data": items, "count": len(items) if items is not None else 0}


def save_inventory_item(item_data: dict):
    if not item_data.get("item_name"):
        return {"error": "Item name is required."}

    item_data["last_updated_at"] = datetime.now().isoformat(timespec="seconds")
    item_data["cat_name"] = item_data.get("cat_name", "")
    item_data["username"] = item_data.get("username", "admin")

    try:
        inv_repo.create(item_data)
        return {"message": f"Item '{item_data['item_name']}' saved successfully."}
    except Exception as e:
        return {"error": str(e)}


def delete_inventory_item(item_name: str):
    existing = inv_repo.get_by_name(item_name)
    if not existing:
        return {"error": f"Item '{item_name}' not found."}

    inv_repo.delete(item_name)
    return {"message": f"Item '{item_name}' deleted successfully."}


def assign_item_to_user(item_name: str, username: str):
    existing = inv_repo.get_by_name(item_name)
    if not existing:
        return {"error": f"Item '{item_name}' not found."}

    try:
        inv_repo.assign_user(item_name, username)
        return {"message": f"Item '{item_name}' assigned to {username}."}
    except Exception as e:
        return {"error": str(e)}


def update_item_status(item_name: str, new_status: str):
    """Update the item_status of an inventory item."""
    existing = inv_repo.get_by_name(item_name)
    if not existing:
        return {"error": f"Item '{item_name}' not found."}

    try:
        inv_repo.update_status(item_name, new_status)
        return {"message": f"Status of '{item_name}' updated to '{new_status}'."}
    except Exception as e:
        return {"error": str(e)}

# -----------------
# Analytics functions required by Challenge-3
# -----------------
def get_total_item_count():
    try:
        total = inv_repo.get_total_count()
        return {"total": int(total)}
    except Exception as e:
        return {"error": str(e)}

def get_item_count_by_category(category: str):
    try:
        count = inv_repo.get_count_by_category(category)
        return {"category": category, "count": int(count)}
    except Exception as e:
        return {"error": str(e)}

def get_item_count_by_status(status: str):
    try:
        count = inv_repo.get_count_by_status(status)
        return {"status": status, "count": int(count)}
    except Exception as e:
        return {"error": str(e)}

def get_user_with_most_items():
    try:
        top = inv_repo.get_user_with_most_items()
        if not top:
            return {"message": "No users or no items present."}
        return {"username": top["username"], "count": top["count"]}
    except Exception as e:
        return {"error": str(e)}

# -----------------
# Auditing functions required by Challenge-4
# -----------------
def get_last_updated_item():
    """
    Return the inventory item that was most recently updated.
    """
    try:
        item = inv_repo.get_last_updated_item()
        if not item:
            return {"message": "No items with a last_updated_at timestamp found."}
        return {"data": item}
    except Exception as e:
        return {"error": str(e)}

def get_items_not_updated_in_last_n_days(n_days: int = 90):
    """
    Returns items not updated in the last `n_days`. Defaults to 90 days (~3 months).
    """
    try:
        cutoff = datetime.now() - timedelta(days=n_days)
        cutoff_iso = cutoff.isoformat(timespec="seconds")
        items = inv_repo.get_items_not_updated_since(cutoff_iso)
        return {"cutoff": cutoff_iso, "count": len(items) if items is not None else 0, "data": items}
    except Exception as e:
        return {"error": str(e)}

def get_users_with_most_low_status_items(limit: int = 10):
    """
    Returns a normalized list of users and counts of their 'low' status items.
    """
    try:
        rows = inv_repo.get_users_with_most_low_status_items(limit=limit)
        if not rows:
            return {"message": "No low-status items or no users found."}

        result = []
        for r in rows:
            if isinstance(r, dict):
                username = r.get("username")
                cnt = int(r.get("cnt", 0))
            else:
                username, cnt = r[0], int(r[1])
            result.append({"username": username, "low_count": cnt})
        return {"data": result}
    except Exception as e:
        return {"error": str(e)}
