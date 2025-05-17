from typing import Any, Dict, List, Optional

class ConversationState:
    def __init__(
        self,
        user_input: str,
        context: Optional[Dict[str, Any]] = None,
        memory: Optional[Dict[str, Any]] = None,
        history: Optional[List[Dict[str, Any]]] = None,
        session_id: Optional[str] = None,
        sentiment: Optional[Dict[str, Any]] = None
    ):
        self.user_input = user_input
        self.context = context or {}
        self.memory = memory or {}
        self.history = history or []
        self.session_id = session_id
        self.sentiment = sentiment or {}
        
    def update_history(self, entry: Dict[str, Any]):
        """Update conversation history with a new entry."""
        self.history.append(entry)
    
    def update_sentiment(self, sentiment_data: Dict[str, Any]):
        """Update sentiment analysis data."""
        self.sentiment = sentiment_data
