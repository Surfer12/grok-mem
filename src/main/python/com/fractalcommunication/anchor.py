from typing import Any
from com.fractalcommunication.interfaces import IAnchor

class ConnectionAnchor(IAnchor):
    def name(self) -> str:
        return "connection"

    def apply(self, reflection: str, state: Any) -> str:
        return reflection + " Let's focus on warmth and mutual understanding."
    
    def get_focus(self) -> str:
        return "warmth and mutual understanding"
    
    def get_action(self) -> str:
        return "notice the connection between your thoughts and feelings"
    
    def get_benefit(self) -> str:
        return "maintain connection even when expressing difficult emotions"

    def microtest(self) -> bool:
        # Ensure key phrase is present
        out = self.apply("test", None)
        return "warmth" in out and "understanding" in out

class GroundingAnchor(IAnchor):
    def name(self) -> str:
        return "grounding"

    def apply(self, reflection: str, state: Any) -> str:
        return reflection + " Take a slow, grounding breath now."
    
    def get_focus(self) -> str:
        return "grounding and staying present"
    
    def get_action(self) -> str:
        return "take a slow, deep breath before responding"
    
    def get_benefit(self) -> str:
        return "navigate challenges with clarity and calm"

    def microtest(self) -> bool:
        out = self.apply("test", None)
        return "grounding breath" in out

class OpennessAnchor(IAnchor):
    def name(self) -> str:
        return "openness"

    def apply(self, reflection: str, state: Any) -> str:
        return reflection + " Approach this with curiosity, without judgment."
    
    def get_focus(self) -> str:
        return "openness and curiosity"
    
    def get_action(self) -> str:
        return "approach conversations with a beginner's mind"
    
    def get_benefit(self) -> str:
        return "discover new perspectives and solutions"

    def microtest(self) -> bool:
        out = self.apply("test", None)
        return "curiosity" in out and "judgment" in out
