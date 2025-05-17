#!/usr/bin/env python3
# A/B Testing Framework for Fractal Communication Framework

from typing import Dict, List, Tuple, Any, Callable, Optional
import random
import statistics
import time
import json
from pathlib import Path

from com.fractalcommunication.orchestrator import Orchestrator
from com.fractalcommunication.anchor_module import AnchorModule
from com.fractalcommunication.persona import Persona

class ABTest:
    """
    A/B testing framework for comparing different configurations of the
    Fractal Communication Framework.
    """
    
    def __init__(
        self,
        name: str,
        variant_a: Dict[str, Any],
        variant_b: Dict[str, Any],
        evaluation_metric: Callable[[str, Dict[str, Any]], float],
        personas: Optional[Dict[str, Persona]] = None
    ):
        """
        Initialize a new A/B test.
        
        Args:
            name: Name of this test
            variant_a: Configuration for Variant A
            variant_b: Configuration for Variant B
            evaluation_metric: Function that evaluates responses and returns a score
            personas: Optional dictionary of personas for testing
        """
        self.name = name
        self.variant_a = variant_a
        self.variant_b = variant_b
        self.evaluation_metric = evaluation_metric
        self.personas = personas or Persona.create_standard_personas()
        
        # Results storage
        self.results = {
            "a": {"scores": [], "times": [], "responses": []},
            "b": {"scores": [], "times": [], "responses": []}
        }
        
        # Track prompts used in testing
        self.test_prompts = []
        
    def setup_variant(self, variant_config: Dict[str, Any]) -> Orchestrator:
        """
        Set up an orchestrator with the given variant configuration.
        
        Args:
            variant_config: Dictionary containing variant configuration
            
        Returns:
            Configured Orchestrator instance
        """
        # Create anchor module
        anchor_module = AnchorModule()
        
        # Register anchors
        for anchor in variant_config.get("anchors", []):
            anchor_module.register_anchor(anchor)
            
        # Create orchestrator with this anchor module
        return Orchestrator(anchor_module=anchor_module)
        
    def run_test(self, num_trials: int = 10, random_seed: Optional[int] = None) -> Dict[str, Any]:
        """
        Run A/B test with the specified number of trials.
        
        Args:
            num_trials: Number of test prompts to use
            random_seed: Optional seed for reproducibility
            
        Returns:
            Dictionary with test results
        """
        if random_seed is not None:
            random.seed(random_seed)
            
        # Setup variants
        variant_a_orchestrator = self.setup_variant(self.variant_a)
        variant_b_orchestrator = self.setup_variant(self.variant_b)
        
        # Create session IDs
        session_a = f"session_a_{int(time.time())}"
        session_b = f"session_b_{int(time.time())}"
        
        # Generate test prompts from personas if not already set
        if not self.test_prompts:
            for _ in range(num_trials):
                # Select random persona
                persona = random.choice(list(self.personas.values()))
                
                # Generate prompt
                prompt = persona.generate_prompt()
                
                # Store prompt with persona info
                self.test_prompts.append({
                    "text": prompt,
                    "persona": persona.name
                })
        
        # Run tests
        print(f"\n=== Running A/B Test: {self.name} ===\n")
        
        for i, prompt_data in enumerate(self.test_prompts):
            prompt = prompt_data["text"]
            persona_name = prompt_data["persona"]
            persona = self.personas[persona_name]
            
            print(f"\nTest {i+1}/{len(self.test_prompts)} - Persona: {persona_name}")
            print(f"Prompt: {prompt}")
            
            # Test variant A
            start_time = time.time()
            response_a = variant_a_orchestrator.run_conversation(prompt, "test_user", session_a)
            time_a = time.time() - start_time
            
            # Test variant B
            start_time = time.time()
            response_b = variant_b_orchestrator.run_conversation(prompt, "test_user", session_b)
            time_b = time.time() - start_time
            
            # Evaluate responses
            score_a = self.evaluation_metric(response_a, {"prompt": prompt, "persona": persona})
            score_b = self.evaluation_metric(response_b, {"prompt": prompt, "persona": persona})
            
            # Add optional persona-specific evaluation
            persona_score_a = persona.evaluate_response(response_a)
            persona_score_b = persona.evaluate_response(response_b)
            
            # Store results
            self.results["a"]["scores"].append(score_a)
            self.results["a"]["times"].append(time_a)
            self.results["a"]["responses"].append({
                "prompt": prompt,
                "response": response_a,
                "score": score_a,
                "persona_score": persona_score_a,
                "persona": persona_name
            })
            
            self.results["b"]["scores"].append(score_b)
            self.results["b"]["times"].append(time_b)
            self.results["b"]["responses"].append({
                "prompt": prompt,
                "response": response_b,
                "score": score_b,
                "persona_score": persona_score_b,
                "persona": persona_name
            })
            
            # Print comparison
            print(f"\nVariant A - Score: {score_a:.2f}, Persona: {persona_score_a:.2f}, Time: {time_a:.4f}s")
            print(f"Response: {response_a[:100]}...")
            print(f"\nVariant B - Score: {score_b:.2f}, Persona: {persona_score_b:.2f}, Time: {time_b:.4f}s")
            print(f"Response: {response_b[:100]}...")
            
            if score_a > score_b:
                print("\nResult: Variant A performed better")
            elif score_b > score_a:
                print("\nResult: Variant B performed better") 
            else:
                print("\nResult: Variants performed equally")
        
        # Summarize results
        summary = self.summarize_results()
        
        # Save results
        self.save_results()
        
        return summary
        
    def summarize_results(self) -> Dict[str, Any]:
        """
        Summarize test results with statistical analysis.
        
        Returns:
            Dictionary with summary statistics
        """
        # Calculate summary statistics
        a_scores = self.results["a"]["scores"]
        b_scores = self.results["b"]["scores"]
        
        a_times = self.results["a"]["times"]
        b_times = self.results["b"]["times"]
        
        # Calculate means
        a_score_mean = statistics.mean(a_scores) if a_scores else 0
        b_score_mean = statistics.mean(b_scores) if b_scores else 0
        
        a_time_mean = statistics.mean(a_times) if a_times else 0
        b_time_mean = statistics.mean(b_times) if b_times else 0
        
        # Calculate per-persona results
        persona_results = {}
        
        for persona_name in self.personas:
            # Get all responses for this persona
            a_persona_responses = [r for r in self.results["a"]["responses"] if r["persona"] == persona_name]
            b_persona_responses = [r for r in self.results["b"]["responses"] if r["persona"] == persona_name]
            
            # Calculate mean scores
            a_persona_scores = [r["persona_score"] for r in a_persona_responses]
            b_persona_scores = [r["persona_score"] for r in b_persona_responses]
            
            a_persona_mean = statistics.mean(a_persona_scores) if a_persona_scores else 0
            b_persona_mean = statistics.mean(b_persona_scores) if b_persona_scores else 0
            
            # Determine winner for this persona
            winner = "A" if a_persona_mean > b_persona_mean else "B" if b_persona_mean > a_persona_mean else "Tie"
            
            persona_results[persona_name] = {
                "a_mean": a_persona_mean,
                "b_mean": b_persona_mean,
                "winner": winner,
                "difference": abs(a_persona_mean - b_persona_mean)
            }
        
        # Determine overall winner
        if a_score_mean > b_score_mean:
            winner = "A"
            improvement = ((a_score_mean - b_score_mean) / b_score_mean) * 100 if b_score_mean else 0
        elif b_score_mean > a_score_mean:
            winner = "B"
            improvement = ((b_score_mean - a_score_mean) / a_score_mean) * 100 if a_score_mean else 0
        else:
            winner = "Tie"
            improvement = 0
            
        # Create summary
        summary = {
            "test_name": self.name,
            "total_trials": len(self.test_prompts),
            "a_name": self.variant_a.get("name", "Variant A"),
            "b_name": self.variant_b.get("name", "Variant B"),
            "a_score_mean": a_score_mean,
            "b_score_mean": b_score_mean,
            "a_time_mean": a_time_mean,
            "b_time_mean": b_time_mean,
            "winner": winner,
            "improvement_percent": improvement,
            "per_persona": persona_results
        }
        
        # Print summary
        print("\n=== Test Summary ===")
        print(f"Test: {self.name}")
        print(f"Trials: {len(self.test_prompts)}")
        print(f"\nVariant A ({self.variant_a.get('name', 'Variant A')}):")
        print(f"  Mean Score: {a_score_mean:.2f}")
        print(f"  Mean Response Time: {a_time_mean:.4f}s")
        print(f"\nVariant B ({self.variant_b.get('name', 'Variant B')}):")
        print(f"  Mean Score: {b_score_mean:.2f}")
        print(f"  Mean Response Time: {b_time_mean:.4f}s")
        print(f"\nWinner: Variant {winner}")
        if winner != "Tie":
            print(f"Improvement: {improvement:.2f}%")
            
        print("\nPer-Persona Results:")
        for persona, result in persona_results.items():
            print(f"  {persona.capitalize()}: Variant {result['winner']} " + 
                  f"(A: {result['a_mean']:.2f}, B: {result['b_mean']:.2f})")
        
        return summary
        
    def save_results(self, directory: str = "test_results"):
        """
        Save test results to a file.
        
        Args:
            directory: Directory to save results in
        """
        # Create directory if it doesn't exist
        Path(directory).mkdir(parents=True, exist_ok=True)
        
        # Create filename with timestamp
        timestamp = int(time.time())
        filename = f"{directory}/{self.name}_{timestamp}.json"
        
        # Create full results object
        full_results = {
            "test_name": self.name,
            "timestamp": timestamp,
            "variant_a": {
                "name": self.variant_a.get("name", "Variant A"),
                "config": {k: str(v) for k, v in self.variant_a.items() if k != "anchors"}
            },
            "variant_b": {
                "name": self.variant_b.get("name", "Variant B"),
                "config": {k: str(v) for k, v in self.variant_b.items() if k != "anchors"}
            },
            "prompts": self.test_prompts,
            "results": {
                "a": {
                    "scores": self.results["a"]["scores"],
                    "times": self.results["a"]["times"],
                    "responses": self.results["a"]["responses"]
                },
                "b": {
                    "scores": self.results["b"]["scores"],
                    "times": self.results["b"]["times"],
                    "responses": self.results["b"]["responses"]
                }
            },
            "summary": self.summarize_results()
        }
        
        # Save to file
        with open(filename, 'w') as f:
            json.dump(full_results, f, indent=2)
            
        print(f"\nResults saved to: {filename}")
        
# Example evaluation metrics
def simple_length_metric(response: str, context: Dict[str, Any] = None) -> float:
    """Simple metric that scores based on response length (longer is better)."""
    return min(1.0, len(response) / 500)  # Normalize to 0.0-1.0

def persona_satisfaction_metric(response: str, context: Dict[str, Any]) -> float:
    """Use persona's own evaluation of the response."""
    if "persona" in context and hasattr(context["persona"], "evaluate_response"):
        return context["persona"].evaluate_response(response)
    return 0.5  # Default neutral score

def keyword_presence_metric(response: str, context: Dict[str, Any]) -> float:
    """Score based on presence of desired keywords."""
    keywords = ["connection", "warmth", "understanding", "curiosity", 
                "perspective", "grounding", "breath", "present", "calm"]
    
    # Count keyword occurrences
    score = sum(1 for keyword in keywords if keyword.lower() in response.lower()) / len(keywords)
    return score
    
def compound_metric(response: str, context: Dict[str, Any]) -> float:
    """Combine multiple metrics for a more balanced score."""
    # Weights for different metrics
    weights = {
        "persona": 0.6,
        "keywords": 0.3,
        "length": 0.1
    }
    
    # Calculate individual scores
    persona_score = persona_satisfaction_metric(response, context)
    keyword_score = keyword_presence_metric(response, context)
    length_score = simple_length_metric(response, context)
    
    # Combine scores using weights
    return (
        weights["persona"] * persona_score +
        weights["keywords"] * keyword_score +
        weights["length"] * length_score
    )