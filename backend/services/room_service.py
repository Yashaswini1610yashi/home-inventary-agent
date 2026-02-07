# services/room_service.py
from repos.room_repo import RoomRepo
from core.db import memory_db

room_repo = RoomRepo()
room_repo.create_table()

def create_room(room_name: str, floor_no: int):
    """Create a new room."""
    existing = room_repo.get_by_name(room_name)
    if existing:
        return {"message": f"Room '{room_name}' already exists."}
    room_repo.create(room_name, floor_no)
    return {"message": f"Room '{room_name}' added successfully."}

def get_all_rooms():
    """Fetch all room details."""
    return {"data": room_repo.get_all()}

def get_item_count_by_room(room_name: str):
    """Return number of items in a room."""
    query = "SELECT COUNT(*) AS count FROM inventory WHERE room_name = ?"
    result = memory_db.fetch_one(query, (room_name,))
    return {"room_name": room_name, "count": result["count"] if result else 0}

def get_room_with_highest_high_status_items():
    """Find room with highest number of items having 'high' status."""
    query = """
    SELECT room_name, COUNT(*) AS high_count
    FROM inventory
    WHERE LOWER(item_status) = 'high'
    GROUP BY room_name
    ORDER BY high_count DESC
    LIMIT 1
    """
    result = memory_db.fetch_one(query)
    if not result:
        return {"message": "No rooms with 'high' condition items found."}
    return {"room_name": result["room_name"], "high_count": result["high_count"]}

def get_user_recently_updated_room(room_name: str):
    """Find the user who most recently updated an item in a given room."""
    query = """
    SELECT username, item_name, last_updated_at
    FROM inventory
    WHERE room_name = ?
    ORDER BY last_updated_at DESC
    LIMIT 1
    """
    result = memory_db.fetch_one(query, (room_name,))
    if not result:
        return {"message": f"No updates found for room '{room_name}'."}
    return {
        "room_name": room_name,
        "username": result["username"],
        "item_name": result["item_name"],
        "last_updated_at": result["last_updated_at"]
    }
