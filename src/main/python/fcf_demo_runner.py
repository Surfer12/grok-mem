#!/usr/bin/env python3
# Fractal Communication Framework Demo Runner

import sys
import os
import argparse
from pathlib import Path

# Add the src/main/python directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Fractal Communication Framework Demo Runner")
    parser.add_argument("--mode", choices=["standard", "ab_test", "all"], default="standard",
                      help="Demo mode: standard, ab_test, or all")
    parser.add_argument("--trials", type=int, default=8,
                      help="Number of trials for A/B testing")
    parser.add_argument("--persona", choices=["analytical", "emotional", "anxious", "practical", "all"], 
                      default="all", help="Specific persona to use for testing")
    parser.add_argument("--output", help="Output directory for results",
                      default=str(Path.home() / "fcf_results"))
    
    args = parser.parse_args()
    
    # Create output directory
    os.makedirs(args.output, exist_ok=True)
    
    # Import modules based on requested mode
    if args.mode in ["standard", "all"]:
        from com.fractalcommunication.demo import main as standard_demo
        print("\n=== Running Standard Demo ===\n")
        standard_demo()
        
    if args.mode in ["ab_test", "all"]:
        from com.fractalcommunication.demo_ab import main as ab_test_demo
        from com.fractalcommunication.metrics_collector import MetricsCollector
        
        print("\n=== Running A/B Testing Demo ===\n")
        
        # Create metrics collector
        metrics_dir = os.path.join(args.output, "metrics")
        metrics = MetricsCollector(output_dir=metrics_dir)
        
        # Run demo with metrics collection
        ab_test_demo(trials=args.trials, persona=args.persona, metrics=metrics)
        
        # Generate metrics report
        report_path = metrics.export_metrics_report()
        print(f"\nDetailed metrics report saved to: {report_path}")
    
    print("\n=== All Demos Complete ===\n")
    print(f"Results stored in: {args.output}")

if __name__ == "__main__":
    main()