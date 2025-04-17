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
        """Basic selection logic; can be extended for more sophisticated selection."""
        if not self._anchors:
            return None
            
        # Simple selection logic based on history size
        index = len(state.history) % len(self._anchors)
        anchor_name = list(self._anchors.keys())[index]
        return self._anchors.get(anchor_name)

    def run_microtests(self) -> Dict[str, bool]:
        """Run each anchor's micro-test and report pass/fail."""
        return {
            name: anchor.microtest()
            for name, anchor in self._anchors.items()
        }
        
    def get_anchor_names(self) -> List[str]:
        """Get list of available anchor names."""
        return list(self._anchors.keys())