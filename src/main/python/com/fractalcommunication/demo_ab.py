#!/usr/bin/env python3
# A/B Testing Demo for Fractal Communication Framework

from com.fractalcommunication.orchestrator import Orchestrator
from com.fractalcommunication.anchor import ConnectionAnchor, GroundingAnchor, OpennessAnchor
from com.fractalcommunication.anchor_module import AnchorModule
from com.fractalcommunication.persona import Persona
from com.fractalcommunication.ab_testing import ABTest, compound_metric
from com.fractalcommunication.metrics_collector import MetricsCollector
from typing import Optional, Dict
import time
import os

# Custom anchors for variant testing
class EnhancedConnectionAnchor(ConnectionAnchor):
    def name(self) -> str:
        return "enhanced_connection"
    
    def apply(self, reflection: str, state: any) -> str:
        return reflection + " Try to validate others' emotions first before sharing your own."
    
    def get_focus(self) -> str:
        return "deep emotional connection"
    
    def get_action(self) -> str:
        return "validate feelings before expressing your own perspective"
    
    def get_benefit(self) -> str:
        return "create stronger emotional bonds even in difficult conversations"
    
    def microtest(self) -> bool:
        out = self.apply("test", None)
        return "validate" in out and "emotions" in out

class EnhancedGroundingAnchor(GroundingAnchor):
    def name(self) -> str:
        return "enhanced_grounding"
    
    def apply(self, reflection: str, state: any) -> str:
        return reflection + " Notice five things you can see right now to anchor yourself in this moment."
    
    def get_focus(self) -> str:
        return "sensory awareness and present-moment focus"
    
    def get_action(self) -> str:
        return "engage your five senses to anchor yourself before responding"
    
    def get_benefit(self) -> str:
        return "remain centered and make clearer decisions even under pressure"
    
    def microtest(self) -> bool:
        out = self.apply("test", None)
        return "five things" in out and "anchor" in out

def main(trials: int = 8, persona: str = "all", metrics: Optional[MetricsCollector] = None):
    print("=== Fractal Communication Framework A/B Testing Demo ===\n")
    
    # Create test directory if it doesn't exist
    os.makedirs("test_results", exist_ok=True)
    
    # Create standard and enhanced variants
    standard_variant = {
        "name": "Standard Anchors",
        "anchors": [ConnectionAnchor(), GroundingAnchor(), OpennessAnchor()]
    }
    
    enhanced_variant = {
        "name": "Enhanced Anchors",
        "anchors": [EnhancedConnectionAnchor(), EnhancedGroundingAnchor(), OpennessAnchor()]
    }
    
    # Create personas - either all or specific one
    if persona == "all":
        personas = Persona.create_standard_personas()
    else:
        personas = {persona: Persona.create_standard_personas()[persona]}
    
    # Create and run A/B test
    ab_test = ABTest(
        name="standard_vs_enhanced",
        variant_a=standard_variant,
        variant_b=enhanced_variant,
        evaluation_metric=compound_metric,
        personas=personas
    )
    
    # Run test with specified number of trials
    results = ab_test.run_test(num_trials=trials)
    
    # Record metrics if collector provided
    if metrics:
        # Record AB test result
        metrics.record_ab_test_result(results)
        
        # Record individual conversation metrics
        for response_data in ab_test.results["a"]["responses"]:
            metrics.record_conversation_metrics(
                user_input=response_data["prompt"],
                response=response_data["response"],
                anchor_name="standard",  # Simplified for demo
                sentiment={"label": "UNKNOWN", "score": 0.0},  # Would need to extract from actual response
                times={"total": 0.1},  # Simplified for demo
                session_id="a_test_session",
                persona_name=response_data["persona"],
                satisfaction_score=response_data["persona_score"]
            )
            
        for response_data in ab_test.results["b"]["responses"]:
            metrics.record_conversation_metrics(
                user_input=response_data["prompt"],
                response=response_data["response"],
                anchor_name="enhanced",  # Simplified for demo
                sentiment={"label": "UNKNOWN", "score": 0.0},  # Would need to extract from actual response
                times={"total": 0.1},  # Simplified for demo
                session_id="b_test_session",
                persona_name=response_data["persona"],
                satisfaction_score=response_data["persona_score"]
            )
    
    # Print overall recommendation
    print("\n=== Final Recommendation ===")
    if results["winner"] == "A":
        print(f"Recommendation: Continue using {standard_variant['name']}")
        if results["improvement_percent"] > 10:
            print(f"The standard variant performed {results['improvement_percent']:.1f}% better overall")
        else:
            print("The difference was minor, consider further testing")
    elif results["winner"] == "B":
        print(f"Recommendation: Switch to {enhanced_variant['name']}")
        if results["improvement_percent"] > 10:
            print(f"The enhanced variant performed {results['improvement_percent']:.1f}% better overall")
        else:
            print("The difference was minor, consider further testing")
    else:
        print("Both variants performed equally well")
        print("Consider other factors like implementation cost or maintenance complexity")
    
    # Print persona-specific recommendations
    print("\nPersona-Specific Recommendations:")
    for persona_name, data in results["per_persona"].items():
        if data["winner"] == "A":
            print(f"- For {persona_name} users: Use {standard_variant['name']}")
        elif data["winner"] == "B":
            print(f"- For {persona_name} users: Use {enhanced_variant['name']}")
        else:
            print(f"- For {persona_name} users: Either variant works equally well")
    
if __name__ == "__main__":
    main()