from typing import Any
from com.fractalcommunication.interfaces import IAnchor

class ConnectionAnchor(IAnchor):
    def name(self) -> str:
        return "connection"

    def apply(self, reflection: str, state: Any) -> str:
        return reflection + " Let's focus on warmth and mutual understanding."

    def microtest(self) -> bool:
        # Ensure key phrase is present
        out = self.apply("test", None)
        return "warmth" in out and "understanding" in out

class GroundingAnchor(IAnchor):
    def name(self) -> str:
        return "grounding"

    def apply(self, reflection: str, state: Any) -> str:
        return reflection + " Take a slow, grounding breath now."

    def microtest(self) -> bool:
        out = self.apply("test", None)
        return "grounding breath" in out

class OpennessAnchor(IAnchor):
    def name(self) -> str:
        return "openness"

    def apply(self, reflection: str, state: Any) -> str:
        return reflection + " Approach this with curiosity, without judgment."

    def microtest(self) -> bool:
        out = self.apply("test", None)
        return "curiosity" in out and "judgment" in out