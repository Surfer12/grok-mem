from com.fractalcommunication.interfaces import IReflectionEngine
from com.fractalcommunication.state import ConversationState

class ReflectionEngine(IReflectionEngine):
    def reflect(self, state: ConversationState) -> str:
        # Simple pattern: echo and elaborate
        return f"You mentioned: '{state.user_input}'. Let's explore what underlying needs or patterns might be present."

    def get_reflection_metrics(self) -> dict:
        """Return metrics about reflections performed."""
        return {"reflectionsPerformed": 1}