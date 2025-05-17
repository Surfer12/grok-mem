#!/usr/bin/env python3
# Orchestrator for Fractal Communication Framework

from com.fractalcommunication.reflection import ReflectionEngine
from com.fractalcommunication.anchor_module import AnchorModule
from com.fractalcommunication.synthesis_module import SynthesisModule
from com.fractalcommunication.memory import InMemoryMemory
from com.fractalcommunication.state import ConversationState
from com.fractalcommunication.sentiment_analyzer import SentimentAnalyzer
import time

class Orchestrator:
    def __init__(self, anchor_module: AnchorModule):
        self.reflection_engine = ReflectionEngine()
        self.anchor_module = anchor_module
        self.synthesis_module = SynthesisModule()
        self.memory_module = InMemoryMemory()
        self.sentiment_analyzer = SentimentAnalyzer()
    
    def run_conversation(self, user_input: str, user_id: str, session_id: str) -> str:
        metrics = {"times": {}}
        
        # Step 1: Analyze sentiment
        start_time = time.time()
        sentiment_data = self.sentiment_analyzer.analyze(user_input)
        metrics["times"]["sentiment_analysis"] = time.time() - start_time
        
        # Step 2: Create a ConversationState object with user input and sentiment
        state = ConversationState(
            user_input=user_input, 
            session_id=session_id,
            sentiment=sentiment_data
        )
        
        # Step 3: Reflect on input using the state object
        start_time = time.time()
        reflection = self.reflection_engine.reflect(state)
        metrics["times"]["reflection"] = time.time() - start_time
        
        # Step 4: Select anchor based on sentiment and content
        start_time = time.time()
        anchor = self.anchor_module.select_anchor(state)
        metrics["times"]["anchor_selection"] = time.time() - start_time
        
        # Get anchor name as a string
        anchor_name = anchor.name()
        
        # Step 5: Synthesize response with explicit anchor name
        start_time = time.time()
        response = self.synthesis_module.synthesize(
            reflection=reflection,
            anchor=anchor,
            anchor_name=anchor_name,
            user_history=self.memory_module.get_short_term()
        )
        metrics["times"]["synthesis"] = time.time() - start_time
        
        # Step 6: Update memory with the conversation
        self.memory_module.update(
            key=f"conversation_{len(state.history)}",
            value={
                "user_input": user_input,
                "response": response,
                "sentiment": sentiment_data,
                "anchor": anchor_name
            },
            scope="short_term"
        )
        
        # Log metrics
        self._log_metrics(user_input, response, anchor_name, sentiment_data, metrics)
        
        return response
    
    def _log_metrics(self, input_text: str, output_text: str, anchor_name: str, sentiment: dict = None, metrics: dict = None):
        """Log detailed metrics about the conversation."""
        # Log basic metrics
        print(f"[Metrics] Reflection: {len(input_text)} characters")
        print(f"[Metrics] Anchor: {anchor_name}, Success: True")
        print(f"[Metrics] Outcome: {len(output_text)} characters")
        
        # Log sentiment if available
        if sentiment:
            print(f"[Metrics] Sentiment: {sentiment['label']}, Score: {sentiment['score']:.2f}")
        
        # Log timing metrics if available
        if metrics and "times" in metrics:
            for step, duration in metrics["times"].items():
                print(f"[Metrics] Time ({step}): {duration:.4f}s")
            
            # Log total processing time
            total_time = sum(metrics["times"].values())
            print(f"[Metrics] Total processing time: {total_time:.4f}s")
