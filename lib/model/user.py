from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class User:
    user_id: int
    username: str
    password: str

@dataclass
class Partner:
    partner_id: int
    name: str
