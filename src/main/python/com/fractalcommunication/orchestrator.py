#!/usr/bin/env python3
# Orchestrator for Fractal Communication Framework

from com.fractalcommunication.reflection import ReflectionEngine
from com.fractalcommunication.anchor_module import AnchorModule
from com.fractalcommunication.synthesis_module import SynthesisModule
from com.fractalcommunication.memory import InMemoryMemory
from com.fractalcommunication.state import ConversationState

class Orchestrator:
    def __init__(self, anchor_module: AnchorModule):
        self.reflection_engine = ReflectionEngine()
        self.anchor_module = anchor_module
        self.synthesis_module = SynthesisModule()
        self.memory_module = InMemoryMemory()
    
    def run_conversation(self, user_input: str, user_id: str, session_id: str) -> str:
        # Step 1: Create a ConversationState object with user input
        state = ConversationState(user_input=user_input, session_id=session_id)
        
        # Step 2: Reflect on input using the state object
        reflection = self.reflection_engine.reflect(state)
        
        # Step 3: Select anchor
        anchor = self.anchor_module.select_anchor(state)
        
        # Step 4: Synthesize response with explicit anchor name
        response = self.synthesis_module.synthesize(
            reflection=reflection,
            anchor=anchor,
            anchor_name=anchor.name,
            user_history=self.memory_module.get_short_term()
        )
        
        # Log metrics
        self._log_metrics(user_input, response, anchor.name)
        
        return response
    
    def _log_metrics(self, input_text: str, output_text: str, anchor_name: str):
        # Placeholder for metrics logging
        print(f"[Metrics] Reflection: {len(input_text)} characters")
        print(f"[Metrics] Anchor: {anchor_name}, Success: True")
        print(f"[Metrics] Outcome: {len(output_text)} characters")
EOF 2>&1
