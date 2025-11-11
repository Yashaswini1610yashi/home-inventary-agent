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
    tools=[fetch_all_inv],
)
