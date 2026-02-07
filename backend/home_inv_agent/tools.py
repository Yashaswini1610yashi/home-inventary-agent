# tools.py
# keep the same names as your original tools file but import corrected services
from services.inventory_service import *
from services.room_service import *

# Re-export functions used by your agent (same signatures)
def fetch_all_inv() -> dict:
    return get_all_inventory()

def fetch_by_category(cat_name: str) -> dict:
    return get_inventory_by_category(cat_name)

def fetch_by_status(status: str) -> dict:
    return get_inventory_by_status(status)

def check_item_exists(item_name: str) -> dict:
    return get_inventory_by_name(item_name)

def assign_item_to_user_tool(item_name: str, user_name: str) -> dict:
    return assign_item_to_user(item_name, user_name)

def update_item_status_tool(item_name: str, new_status: str) -> dict:
    return update_item_status(item_name, new_status)

def remove_item_tool(item_name: str) -> dict:
    return delete_inventory_item(item_name)

def save_item(items: dict):
    return save_inventory_item(items)

# Analytics
def get_total_items_tool() -> dict:
    return get_total_item_count()

def get_category_item_count_tool(category: str) -> dict:
    return get_item_count_by_category(category)

def get_status_item_count_tool(status: str) -> dict:
    return get_item_count_by_status(status)

def get_top_user_tool() -> dict:
    return get_user_with_most_items()

# Auditing
def get_last_updated_item_tool() -> dict:
    return get_last_updated_item()

def get_items_not_updated_in_last_3_months_tool() -> dict:
    # agent calls this without arguments; internal service uses 90 days default
    return get_items_not_updated_in_last_n_days(90)

def get_users_with_most_low_status_items_tool(limit: int) -> dict:
    # no default here; agent must supply an integer.
    return get_users_with_most_low_status_items(limit=limit)

# Room / Multi-modal Operations
def add_room(room_name: str, floor_no: int):
    """Create a new room."""
    return create_room(room_name, floor_no)

def all_rooms():
    """List all rooms."""
    return get_all_rooms()

def item_count_in_room(room_name: str):
    """Count how many items are in a specific room."""
    return get_item_count_by_room(room_name)

def room_with_most_high_condition_items():
    """Find the room with the most high-condition items."""
    return get_room_with_highest_high_status_items()

def user_who_recently_updated_room(room_name: str):
    """Find which user last updated items in a given room."""
    return get_user_recently_updated_room(room_name)
