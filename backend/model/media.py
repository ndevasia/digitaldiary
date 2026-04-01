from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class Media:
    media_id: int
    type: str  # e.g., 'video', 'screenshot', 'audio'
    media_url: str
    timestamp: datetime
    owner_user_id: str
    app_name: Optional[str] = None  # e.g., 'Discord', 'Steam'
    user_with: Optional[str] = None  # e.g., 'Friend Name' or multiple names
    session_id: Optional[str] = None  # Session identifier

@dataclass
class App:
    app_id: int
    app_name: str
    app_url: str
    timestamp: datetime
    owner_user_id: int

@dataclass
class JournalEntry:
    entry_id: int
    text: str
    timestamp: datetime
    owner_user_id: int