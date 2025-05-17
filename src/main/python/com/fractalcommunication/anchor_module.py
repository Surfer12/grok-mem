from typing import Dict, Optional, List
from com.fractalcommunication.interfaces import IAnchor, IAnchorModule
from com.fractalcommunication.state import ConversationState

class AnchorModule(IAnchorModule):
    def __init__(self):
        self._anchors: Dict[str, IAnchor] = {}

    def register_anchor(self, anchor: IAnchor):
        """Register a new Anchor plug-in."""
        self._anchors[anchor.name()] = anchor
        print(f"Registered anchor: {anchor.name()}")

    def select_anchor(self, state: ConversationState) -> Optional[IAnchor]:
        """Select an anchor based on sentiment analysis and user input content."""
        if not self._anchors:
            return None
            
        # Default to cycling through anchors based on history size if no specific context matches
        default_index = len(state.history) % len(self._anchors)
        default_anchor_name = list(self._anchors.keys())[default_index]
        
        # First, check if sentiment data is available
        if state.sentiment and 'label' in state.sentiment:
            # Use sentiment-based anchor selection
            if state.sentiment['label'] == 'NEGATIVE' and state.sentiment['score'] > 0.7:
                # Strong negative sentiment - prioritize grounding
                if "grounding" in self._anchors:
                    return self._anchors.get("grounding")
            elif state.sentiment['label'] == 'NEGATIVE' and state.sentiment['score'] > 0.5:
                # Moderate negative sentiment - prioritize connection
                if "connection" in self._anchors:
                    return self._anchors.get("connection")
            elif state.sentiment['label'] == 'POSITIVE' and state.sentiment['score'] > 0.7:
                # Strong positive sentiment - prioritize openness
                if "openness" in self._anchors:
                    return self._anchors.get("openness")
        
        # Fallback to keyword analysis if sentiment is neutral or not available
        user_input = state.user_input.lower()
        if any(word in user_input for word in ["frustrating", "frustrated", "annoying", "difficult", "hard"]):
            # Prioritize grounding for frustration or difficulty
            if "grounding" in self._anchors:
                return self._anchors.get("grounding")
        elif any(word in user_input for word in ["understand", "perspective", "curious", "learn", "how", "why"]):
            # Prioritize openness for curiosity or learning
            if "openness" in self._anchors:
                return self._anchors.get("openness")
        elif any(word in user_input for word in ["disagreement", "tension", "hurt", "feelings", "worry"]):
            # Prioritize connection for emotional concerns or relational issues
            if "connection" in self._anchors:
                return self._anchors.get("connection")
        
        # Fall back to default cycling if no specific context is matched
        return self._anchors.get(default_anchor_name)

    def run_microtests(self) -> Dict[str, bool]:
        """Run each anchor's micro-test and report pass/fail."""
        return {
            name: anchor.microtest()
            for name, anchor in self._anchors.items()
        }
        
    def get_anchor_names(self) -> List[str]:
        """Get list of available anchor names."""
        return list(self._anchors.keys())
