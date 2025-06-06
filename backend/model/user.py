from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class User:
    user_id: int
    username: str
    password: str
    #default_hero_image_url: Optional[str] = None  # URL of the user's chosen hero image


@dataclass
class Partner:
    user_id: int
    name: str
