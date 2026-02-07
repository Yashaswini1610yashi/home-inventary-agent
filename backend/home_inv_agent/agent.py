# agent.py
from google.adk.agents import LlmAgent 
from home_inv_agent.prompt import *
from home_inv_agent.tools import *

MODEL = "gemini-2.5-flash"

root_agent = LlmAgent(
    name="home_inventory_agent",
    model=MODEL,
    description=(
        "Agent to manage and keep a track of Home Inventory"
    ),
    instruction=ROOT_AGENT_PROMPT,
    tools=[fetch_all_inv, fetch_by_category,fetch_by_status, check_item_exists,assign_item_to_user_tool,update_item_status_tool,remove_item_tool,get_total_items_tool,get_category_item_count_tool,get_status_item_count_tool,get_top_user_tool,get_last_updated_item_tool,get_items_not_updated_in_last_3_months_tool,get_users_with_most_low_status_items_tool, add_room,all_rooms, item_count_in_room, room_with_most_high_condition_items,user_who_recently_updated_room,
    save_item],
)
