from typing import List, Optional
from com.fractalcommunication.interfaces import IOrchestrator
from com.fractalcommunication.reflection import ReflectionEngine
from com.fractalcommunication.anchor_module import AnchorModule
from com.fractalcommunication.synthesis import SynthesisModule
from com.fractalcommunication.memory import InMemoryMemory, UserProfile
from com.fractalcommunication.metrics import SimpleMetricsLogger
from com.fractalcommunication.state import ConversationState

class FCFException(Exception):
    """Base exception for Fractal Communication Framework specific errors."""
    def __init__(self, message: str, cause: Optional[Exception] = None):
        super().__init__(message)
        self.cause = cause

class Orchestrator(IOrchestrator):
    def __init__(
        self, 
        reflection_engine: Optional[ReflectionEngine] = None,
        anchor_module: Optional[AnchorModule] = None,
        synthesis_module: Optional[SynthesisModule] = None,
        memory: Optional[InMemoryMemory] = None,
        metrics_logger: Optional[SimpleMetricsLogger] = None
    ):
        self.reflection_engine = reflection_engine or ReflectionEngine()
        self.anchor_module = anchor_module or AnchorModule()
        self.synthesis_module = synthesis_module or SynthesisModule()
        self.memory = memory or InMemoryMemory()
        self.metrics_logger = metrics_logger or SimpleMetricsLogger()
        self.active_branches = {}

    def run_conversation(self, user_input: str, user_id: str, session_id: Optional[str] = None) -> str:
        # Initialize state to avoid 'possibly unbound' error
        state = ConversationState(user_input=user_input)
        
        try:
            # Load user profile or create a default one
            user_profile = UserProfile(user_id)
            
            # Create conversation state with user profile data
            state = ConversationState(
                user_input=user_input,
                context=user_profile.interaction_style, 
                memory=self.memory.get_short_term(),
                session_id=session_id
            )
            
            # Run reflection
            reflection = self.reflection_engine.reflect(state)
            self.metrics_logger.log_reflection(state, reflection)
            
            # Select and apply anchor
            anchor = self.anchor_module.select_anchor(state)
            if not anchor:
                raise FCFException("No anchor available")
                
            anchored_response = anchor.apply(reflection, state)
            self.metrics_logger.log_anchor(anchor.name(), anchor.microtest(), state)
            
            # Synthesize output
            output = self.synthesis_module.synthesize(reflection, anchored_response, state)
            self.metrics_logger.log_outcome(state, output)
            
            # Save interaction to memory
            if session_id:
                self.memory.update(
                    key=f"interaction_{len(state.history)}",
                    value={
                        "user_input": user_input,
                        "reflection": reflection,
                        "anchor": anchor.name(),
                        "output": output
                    },
                    scope="session",
                    session_id=session_id
                )
            
            # Update history
            state.update_history({
                "user_input": user_input,
                "output": output
            })
            
            return output
        except Exception as e:
            self.metrics_logger.log_error("Orchestrator", f"Conversation error: {str(e)}", e)
            return self.handle_error(e, state)

    def handle_error(self, error: Exception, state: ConversationState) -> str:
        # Fallback or escalation
        return "I'm having trouble processing that. Could you clarify what you mean?"

    def branch(self, state: ConversationState, options: List[str]) -> str:
        # Present options to user or auto-select
        key = f"{state.session_id}"
        self.active_branches.setdefault(key, []).append(options)
        return f"I see a few different ways we could approach this. Would you prefer: {', '.join(options)}?"

    def interrupt(self, state: ConversationState, reason: str) -> str:
        # Handle emotional spike, disengagement, etc.
        key = f"{state.session_id}"
        self.active_branches.setdefault(key, []).append(f"Interruption: {reason}")
        self.metrics_logger.log_error("Orchestrator", f"Interruption: {reason}")
        return f"I notice something important has come up. Let's pause and address {reason}."