from typing import Dict, Any, Optional, List
from com.fractalcommunication.interfaces import IMemory

class InMemoryMemory(IMemory):
    def __init__(self):
        self.short_term = {}
        self.long_term = {}
        self.sessions = {}

    def get_short_term(self) -> Dict[str, Any]:
        return self.short_term

    def get_long_term(self) -> Dict[str, Any]:
        return self.long_term

    def get_session(self, session_id: str) -> Dict[str, Any]:
        return self.sessions.setdefault(session_id, {})

    def update(self, key: str, value: Any, scope: str = "short_term", session_id: Optional[str] = None):
        if scope == "short_term":
            self.short_term[key] = value
        elif scope == "long_term":
            self.long_term[key] = value
        elif scope == "session" and session_id:
            self.sessions.setdefault(session_id, {})[key] = value
            
class UserProfile:
    def __init__(self, user_id: str, interaction_style: Optional[Dict[str, str]] = None, preferred_anchors: Optional[List[str]] = None):
        self.user_id = user_id
        self.interaction_style = interaction_style or {"style": "fractal"}
        self.preferred_anchors = preferred_anchors or ["connection"]
        
    def update_interaction_style(self, new_style: Dict[str, str]):
        self.interaction_style.update(new_style)