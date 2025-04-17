#!/usr/bin/env python3
# Fractal Communication Framework Demo

from com.fractalcommunication.orchestrator import Orchestrator
from com.fractalcommunication.anchor import ConnectionAnchor, GroundingAnchor, OpennessAnchor
from com.fractalcommunication.anchor_module import AnchorModule

def main():
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
    
    # Sample conversation
    user_input = "It's hard to express disagreement without causing tension."
    user_id = "user123"
    session_id = "session456"
    
    print("\n=== Sample Conversation ===")
    print(f"User: {user_input}")
    
    # Run conversation through orchestrator
    response = orchestrator.run_conversation(user_input, user_id, session_id)
    print(f"AI: {response}")
    
    # Continue conversation with a follow-up
    user_input2 = "I worry about hurting the other person's feelings."
    print(f"\nUser: {user_input2}")
    response2 = orchestrator.run_conversation(user_input2, user_id, session_id)
    print(f"AI: {response2}")
    
if __name__ == "__main__":
    main()