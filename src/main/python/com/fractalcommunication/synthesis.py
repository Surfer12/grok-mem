from com.fractalcommunication.interfaces import ISynthesisModule
from com.fractalcommunication.state import ConversationState

class SynthesisModule(ISynthesisModule):
    def synthesize(self, reflection: str, anchored_response: str, state: ConversationState) -> str:
        # Extract anchor name from anchored_response for context-aware synthesis
        anchor_name = ""
        if "grounding" in anchored_response.lower():
            anchor_name = "grounding"
        elif "openness" in anchored_response.lower():
            anchor_name = "openness"
        elif "connection" in anchored_response.lower():
            anchor_name = "connection"
        
        # Default closing advice
        closing_advice = "Try to notice warmth in your heart as you express yourself—this can help maintain connection even in disagreement."
        
        # Vary closing advice based on anchor type for greater response diversity
        if anchor_name == "grounding":
            closing_advice = "Focus on staying centered and calm—this can help you navigate challenges with clarity."
        elif anchor_name == "openness":
            closing_advice = "Embrace this curiosity as a path to growth—this can open new ways of seeing and connecting."
        elif anchor_name == "connection":
            closing_advice = "Hold space for empathy as you share—this can deepen understanding and trust."
        
        # Combine for output
        return f"{anchored_response} {closing_advice}"
        
    def get_synthesis_metrics(self) -> dict:
        """Return metrics about syntheses performed."""
        return {"synthesesPerformed": 1}
