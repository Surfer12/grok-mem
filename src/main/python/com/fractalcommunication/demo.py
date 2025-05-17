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
    
    # Sample conversation with varied inputs
    print("\n=== Sample Conversation ===")
    
    # Scenario 1: Emotional concern about disagreement
    user_input_1 = "It\'s hard to express disagreement without causing tension."
    user_id = "user123"
    session_id = "session456"
    print(f"User: {user_input_1}")
    response_1 = orchestrator.run_conversation(user_input_1, user_id, session_id)
    print(f"AI: {response_1}")
    
    # Scenario 2: Follow-up emotional concern
    user_input_2 = "I worry about hurting the other person\'s feelings."
    print(f"\nUser: {user_input_2}")
    response_2 = orchestrator.run_conversation(user_input_2, user_id, session_id)
    print(f"AI: {response_2}")
    
    # Scenario 3: Curiosity-driven query
    user_input_3 = "How can I better understand different perspectives?"
    print(f"\nUser: {user_input_3}")
    response_3 = orchestrator.run_conversation(user_input_3, user_id, session_id)
    print(f"AI: {response_3}")
    
    # Scenario 4: Frustration or challenge
    user_input_4 = "I keep misunderstanding others, and it\'s frustrating."
    print(f"\nUser: {user_input_4}")
    response_4 = orchestrator.run_conversation(user_input_4, user_id, session_id)
    print(f"AI: {response_4}")
    
    # Scenario 5: Complex request for guidance
    user_input_5 = "Can you help me navigate a tough conversation with a colleague about a missed deadline?"
    print(f"\nUser: {user_input_5}")
    response_5 = orchestrator.run_conversation(user_input_5, user_id, session_id)
    print(f"AI: {response_5}")
    
if __name__ == "__main__":
    main()
