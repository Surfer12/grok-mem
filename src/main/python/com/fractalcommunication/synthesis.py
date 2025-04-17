from com.fractalcommunication.interfaces import ISynthesisModule
from com.fractalcommunication.state import ConversationState

class SynthesisModule(ISynthesisModule):
    def synthesize(self, reflection: str, anchored_response: str, state: ConversationState) -> str:
        # Combine for output
        return f"{anchored_response} Try to notice warmth in your heart as you express yourself—this can help maintain connection even in disagreement."
        
    def get_synthesis_metrics(self) -> dict:
        """Return metrics about syntheses performed."""
        return {"synthesesPerformed": 1}