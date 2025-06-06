from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class Media:
    media_id: int
    type: str  # e.g., 'video', 'screenshot', 'audio'. 'hero_image' is a special type that is not stored in the database.
    #is_hero_image: bool
    media_url: str
    timestamp: datetime
    owner_user_id: int
    game: str # game is optional for hero images
    

@dataclass
class Game:
    game_id: int
    game_name: str
    game_url: str
    timestamp: datetime
    owner_user_id: int

@dataclass
class JournalEntry:
    entry_id: int
    text: str
    timestamp: datetime
    owner_user_id: int