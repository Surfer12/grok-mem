#!/usr/bin/env python3
# Fractal Communication Framework Demo

from com.fractalcommunication.orchestrator import Orchestrator
from com.fractalcommunication.anchor import ConnectionAnchor, GroundingAnchor, OpennessAnchor
from com.fractalcommunication.anchor_module import AnchorModule
import time

def main():
    print("=== Fractal Communication Framework Demo ===\n")
    print("Initializing framework components...")
    
    # Create anchor module and register anchors
    anchor_module = AnchorModule()
    plugin_anchors = [ConnectionAnchor(), GroundingAnchor(), OpennessAnchor()]
    for anchor in plugin_anchors:
        anchor_module.register_anchor(anchor)
        
    # Run micro-tests to ensure anchor safety/efficacy
    results = anchor_module.run_microtests()
    print("\nMicro-test results:")
    for name, passed in results.items():
        status = "PASS" if passed else "FAIL"
        print(f"  - {name}: {status}")
    
    # Create orchestrator with our anchor module
    orchestrator = Orchestrator(anchor_module=anchor_module)
    
    # Define test user and session
    user_id = "user123"
    session_id = f"session_{int(time.time())}"
    
    # Sample conversation with varied inputs (emotion-labeled)
    print("\n=== Sample Conversation with Sentiment Analysis ===\n")
    
    # Test various emotional inputs
    test_inputs = [
        # Positive inputs
        "I'm really excited about learning how to communicate better!",
        
        # Negative inputs
        "I'm feeling very frustrated and overwhelmed with all this conflict.",
        
        # Curiosity-driven inputs
        "How can I better understand different perspectives?",
        
        # Mixed emotional inputs
        "I enjoy talking with my team but sometimes feel anxious about expressing disagreement.",
        
        # Complex request
        "Can you help me navigate a tough conversation with a colleague about a missed deadline?"
    ]
    
    # Run each test input through the framework
    for i, user_input in enumerate(test_inputs):
        print(f"\n--- Test Case {i+1} ---")
        print(f"User: {user_input}")
        
        # Process through orchestrator
        response = orchestrator.run_conversation(user_input, user_id, session_id)
        print(f"AI: {response}\n")
    
    print("=== Demo Complete ===\n")
    print("The Fractal Communication Framework successfully analyzed sentiment")
    print("and adapted responses based on emotional context.")
    
if __name__ == "__main__":
    main()
