from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class User(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    username: str
    firstname: str
    lastname: str
    login_status: str        
    password: str 
    created_at: datetime 


class Category(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    cat_name: str


class Inventory(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    item_name: str
    cat_name: str
    item_status: str        # e.g., "high", "medium", "low"
    comment: Optional[str] = None
    username: str
    last_updated_at: datetime
    created_at: datetime
