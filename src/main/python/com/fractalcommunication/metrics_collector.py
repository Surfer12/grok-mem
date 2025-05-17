#!/usr/bin/env python3
# Metrics Collector for Fractal Communication Framework

from typing import Dict, List, Any, Optional
import time
import json
import os
from datetime import datetime
import statistics
import matplotlib.pyplot as plt
from pathlib import Path

class MetricsCollector:
    """
    Collects, aggregates, and visualizes metrics for the FCF system.
    """
    
    def __init__(self, output_dir: str = "metrics"):
        """
        Initialize the metrics collector.
        
        Args:
            output_dir: Directory to store metrics data and visualizations
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Initialize metrics storage
        self.session_metrics = {}
        self.ab_test_results = []
        self.persona_metrics = {}
        self.anchor_metrics = {}
        
    def record_conversation_metrics(
        self, 
        user_input: str,
        response: str, 
        anchor_name: str,
        sentiment: Dict[str, Any],
        times: Dict[str, float],
        session_id: str,
        persona_name: Optional[str] = None,
        satisfaction_score: Optional[float] = None
    ):
        """
        Record metrics for a single conversation.
        
        Args:
            user_input: User's input text
            response: System's response text
            anchor_name: Name of anchor used
            sentiment: Sentiment analysis results
            times: Dictionary of processing times
            session_id: Session identifier
            persona_name: Optional persona name if in test mode
            satisfaction_score: Optional satisfaction score (0.0-1.0)
        """
        # Create timestamp
        timestamp = int(time.time())
        
        # Create metrics entry
        metrics = {
            "timestamp": timestamp,
            "datetime": datetime.fromtimestamp(timestamp).isoformat(),
            "session_id": session_id,
            "input_length": len(user_input),
            "response_length": len(response),
            "anchor": anchor_name,
            "sentiment": sentiment,
            "processing_times": times,
            "total_time": sum(times.values()),
            "persona": persona_name,
            "satisfaction": satisfaction_score
        }
        
        # Add to session metrics
        if session_id not in self.session_metrics:
            self.session_metrics[session_id] = []
        self.session_metrics[session_id].append(metrics)
        
        # Add to anchor metrics
        if anchor_name not in self.anchor_metrics:
            self.anchor_metrics[anchor_name] = []
        self.anchor_metrics[anchor_name].append(metrics)
        
        # Add to persona metrics if applicable
        if persona_name:
            if persona_name not in self.persona_metrics:
                self.persona_metrics[persona_name] = []
            self.persona_metrics[persona_name].append(metrics)
        
        # Save metrics periodically
        if len(self.session_metrics[session_id]) % 10 == 0:
            self.save_metrics()
    
    def record_ab_test_result(self, test_result: Dict[str, Any]):
        """
        Record results from an A/B test.
        
        Args:
            test_result: Dictionary containing test results
        """
        self.ab_test_results.append(test_result)
        self.save_metrics()
        
    def save_metrics(self):
        """Save current metrics to disk."""
        # Save session metrics
        for session_id, metrics in self.session_metrics.items():
            filename = f"{self.output_dir}/session_{session_id}.json"
            with open(filename, 'w') as f:
                json.dump(metrics, f, indent=2)
                
        # Save AB test results
        if self.ab_test_results:
            filename = f"{self.output_dir}/ab_test_results.json"
            with open(filename, 'w') as f:
                json.dump(self.ab_test_results, f, indent=2)
                
    def generate_summary_report(self) -> Dict[str, Any]:
        """
        Generate a summary report of all collected metrics.
        
        Returns:
            Dictionary with summary statistics
        """
        # Flatten all metrics for overall stats
        all_metrics = []
        for session_metrics in self.session_metrics.values():
            all_metrics.extend(session_metrics)
            
        if not all_metrics:
            return {"error": "No metrics collected"}
            
        # Calculate overall stats
        response_lengths = [m["response_length"] for m in all_metrics]
        processing_times = [m["total_time"] for m in all_metrics]
        
        # Count metrics per anchor
        anchor_counts = {}
        for anchor_name, metrics in self.anchor_metrics.items():
            anchor_counts[anchor_name] = len(metrics)
            
        # Sentiment distribution
        sentiment_counts = {"POSITIVE": 0, "NEGATIVE": 0, "NEUTRAL": 0}
        for m in all_metrics:
            if "sentiment" in m and "label" in m["sentiment"]:
                label = m["sentiment"]["label"]
                sentiment_counts[label] = sentiment_counts.get(label, 0) + 1
                
        # Persona performance if available
        persona_satisfaction = {}
        for persona_name, metrics in self.persona_metrics.items():
            satisfaction_scores = [m.get("satisfaction", 0) for m in metrics if "satisfaction" in m]
            if satisfaction_scores:
                persona_satisfaction[persona_name] = {
                    "mean": statistics.mean(satisfaction_scores),
                    "min": min(satisfaction_scores),
                    "max": max(satisfaction_scores),
                    "count": len(satisfaction_scores)
                }
                
        # AB test summary
        ab_test_summary = {}
        for test in self.ab_test_results:
            test_name = test.get("test_name", "unknown")
            ab_test_summary[test_name] = {
                "winner": test.get("winner", "unknown"),
                "improvement": test.get("improvement_percent", 0),
                "trials": test.get("total_trials", 0)
            }
            
        # Create summary report
        return {
            "total_conversations": len(all_metrics),
            "total_sessions": len(self.session_metrics),
            "response_length": {
                "mean": statistics.mean(response_lengths),
                "min": min(response_lengths),
                "max": max(response_lengths)
            },
            "processing_time": {
                "mean": statistics.mean(processing_times),
                "min": min(processing_times),
                "max": max(processing_times),
                "total": sum(processing_times)
            },
            "anchor_usage": anchor_counts,
            "sentiment_distribution": sentiment_counts,
            "persona_satisfaction": persona_satisfaction,
            "ab_test_summary": ab_test_summary
        }
        
    def generate_visualizations(self):
        """Generate visualizations of collected metrics."""
        # Skip if no metrics
        if not self.session_metrics:
            return
            
        # Create visualizations directory
        viz_dir = f"{self.output_dir}/visualizations"
        os.makedirs(viz_dir, exist_ok=True)
        
        # Flatten all metrics for overall stats
        all_metrics = []
        for session_metrics in self.session_metrics.values():
            all_metrics.extend(session_metrics)
            
        # Skip if no metrics
        if not all_metrics:
            return
            
        # 1. Anchor usage pie chart
        anchor_counts = {}
        for anchor_name, metrics in self.anchor_metrics.items():
            anchor_counts[anchor_name] = len(metrics)
            
        plt.figure(figsize=(10, 6))
        plt.pie(anchor_counts.values(), labels=anchor_counts.keys(), autopct='%1.1f%%')
        plt.title('Anchor Usage Distribution')
        plt.savefig(f"{viz_dir}/anchor_usage_pie.png")
        plt.close()
        
        # 2. Response times by anchor
        anchor_times = {}
        for anchor_name, metrics in self.anchor_metrics.items():
            anchor_times[anchor_name] = [m["total_time"] for m in metrics]
            
        if anchor_times:
            plt.figure(figsize=(12, 6))
            plt.boxplot([times for times in anchor_times.values()], labels=anchor_times.keys())
            plt.title('Response Times by Anchor')
            plt.ylabel('Time (seconds)')
            plt.savefig(f"{viz_dir}/response_times_by_anchor.png")
            plt.close()
            
        # 3. Satisfaction by persona (if available)
        persona_satisfaction = {}
        for persona_name, metrics in self.persona_metrics.items():
            satisfaction_scores = [m.get("satisfaction", 0) for m in metrics if "satisfaction" in m]
            if satisfaction_scores:
                persona_satisfaction[persona_name] = satisfaction_scores
                
        if persona_satisfaction:
            plt.figure(figsize=(12, 6))
            plt.boxplot([scores for scores in persona_satisfaction.values()], 
                        labels=persona_satisfaction.keys())
            plt.title('Satisfaction by Persona')
            plt.ylabel('Satisfaction Score (0-1)')
            plt.savefig(f"{viz_dir}/satisfaction_by_persona.png")
            plt.close()
            
        # 4. A/B test comparison (if available)
        if self.ab_test_results:
            for test in self.ab_test_results:
                test_name = test.get("test_name", "unknown")
                
                # Get mean scores
                a_score = test.get("a_score_mean", 0)
                b_score = test.get("b_score_mean", 0)
                
                # Create bar chart
                plt.figure(figsize=(10, 6))
                plt.bar(['Variant A', 'Variant B'], [a_score, b_score])
                plt.title(f'A/B Test Results: {test_name}')
                plt.ylabel('Mean Score')
                plt.savefig(f"{viz_dir}/ab_test_{test_name}.png")
                plt.close()
                
                # Per-persona results if available
                if "per_persona" in test:
                    persona_data = test["per_persona"]
                    
                    # Extract data
                    personas = list(persona_data.keys())
                    a_scores = [persona_data[p]["a_mean"] for p in personas]
                    b_scores = [persona_data[p]["b_mean"] for p in personas]
                    
                    # Create grouped bar chart
                    plt.figure(figsize=(12, 6))
                    x = range(len(personas))
                    width = 0.35
                    
                    plt.bar([i - width/2 for i in x], a_scores, width, label='Variant A')
                    plt.bar([i + width/2 for i in x], b_scores, width, label='Variant B')
                    
                    plt.xlabel('Persona')
                    plt.ylabel('Mean Score')
                    plt.title(f'A/B Test Results by Persona: {test_name}')
                    plt.xticks(x, personas)
                    plt.legend()
                    
                    plt.savefig(f"{viz_dir}/ab_test_{test_name}_by_persona.png")
                    plt.close()
        
        print(f"Visualizations generated in {viz_dir}")
        
    def export_metrics_report(self):
        """Generate and export a comprehensive metrics report."""
        # Generate summary report
        summary = self.generate_summary_report()
        
        # Save summary
        summary_path = f"{self.output_dir}/summary_report.json"
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)
            
        # Generate visualizations
        self.generate_visualizations()
        
        # Create HTML report
        html_report = self._generate_html_report(summary)
        
        # Save HTML report
        html_path = f"{self.output_dir}/metrics_report.html"
        with open(html_path, 'w') as f:
            f.write(html_report)
            
        print(f"Metrics report generated: {html_path}")
        return html_path
        
    def _generate_html_report(self, summary: Dict[str, Any]) -> str:
        """
        Generate an HTML report from the summary data.
        
        Args:
            summary: Summary data dictionary
            
        Returns:
            HTML string for the report
        """
        # Check for visualization directory
        viz_dir = f"{self.output_dir}/visualizations"
        has_viz = os.path.exists(viz_dir) and len(os.listdir(viz_dir)) > 0
        
        # Start HTML content
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Fractal Communication Framework Metrics Report</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                h1, h2, h3 { color: #333; }
                .summary-box { background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
                .metric-group { margin-bottom: 30px; }
                table { border-collapse: collapse; width: 100%; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
                tr:nth-child(even) { background-color: #f9f9f9; }
                .visualization { margin: 20px 0; text-align: center; }
                .visualization img { max-width: 100%; border: 1px solid #ddd; }
            </style>
        </head>
        <body>
            <h1>Fractal Communication Framework Metrics Report</h1>
            <p>Generated on """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """</p>
            
            <div class="summary-box">
                <h2>Overview</h2>
                <p>Total Conversations: """ + str(summary.get('total_conversations', 0)) + """</p>
                <p>Total Sessions: """ + str(summary.get('total_sessions', 0)) + """</p>
                <p>Average Response Length: """ + str(round(summary.get('response_length', {}).get('mean', 0), 2)) + """ characters</p>
                <p>Average Processing Time: """ + str(round(summary.get('processing_time', {}).get('mean', 0), 4)) + """ seconds</p>
            </div>
            
            <div class="metric-group">
                <h2>Anchor Usage</h2>
                <table>
                    <tr>
                        <th>Anchor</th>
                        <th>Count</th>
                        <th>Percentage</th>
                    </tr>
        """
        
        # Add anchor usage rows
        total_convos = summary.get('total_conversations', 0)
        for anchor, count in summary.get('anchor_usage', {}).items():
            percentage = (count / total_convos * 100) if total_convos > 0 else 0
            html += f"""
                    <tr>
                        <td>{anchor}</td>
                        <td>{count}</td>
                        <td>{percentage:.1f}%</td>
                    </tr>
            """
            
        html += """
                </table>
            </div>
            
            <div class="metric-group">
                <h2>Sentiment Distribution</h2>
                <table>
                    <tr>
                        <th>Sentiment</th>
                        <th>Count</th>
                        <th>Percentage</th>
                    </tr>
        """
        
        # Add sentiment distribution rows
        for sentiment, count in summary.get('sentiment_distribution', {}).items():
            percentage = (count / total_convos * 100) if total_convos > 0 else 0
            html += f"""
                    <tr>
                        <td>{sentiment}</td>
                        <td>{count}</td>
                        <td>{percentage:.1f}%</td>
                    </tr>
            """
            
        html += """
                </table>
            </div>
        """
        
        # Add persona satisfaction if available
        if 'persona_satisfaction' in summary and summary['persona_satisfaction']:
            html += """
            <div class="metric-group">
                <h2>Persona Satisfaction</h2>
                <table>
                    <tr>
                        <th>Persona</th>
                        <th>Mean Score</th>
                        <th>Min Score</th>
                        <th>Max Score</th>
                        <th>Conversations</th>
                    </tr>
            """
            
            for persona, data in summary['persona_satisfaction'].items():
                html += f"""
                        <tr>
                            <td>{persona}</td>
                            <td>{data.get('mean', 0):.2f}</td>
                            <td>{data.get('min', 0):.2f}</td>
                            <td>{data.get('max', 0):.2f}</td>
                            <td>{data.get('count', 0)}</td>
                        </tr>
                """
                
            html += """
                </table>
            </div>
            """
            
        # Add A/B test summary if available
        if 'ab_test_summary' in summary and summary['ab_test_summary']:
            html += """
            <div class="metric-group">
                <h2>A/B Test Results</h2>
                <table>
                    <tr>
                        <th>Test Name</th>
                        <th>Winner</th>
                        <th>Improvement</th>
                        <th>Trials</th>
                    </tr>
            """
            
            for test_name, data in summary['ab_test_summary'].items():
                html += f"""
                        <tr>
                            <td>{test_name}</td>
                            <td>Variant {data.get('winner', 'Unknown')}</td>
                            <td>{data.get('improvement', 0):.2f}%</td>
                            <td>{data.get('trials', 0)}</td>
                        </tr>
                """
                
            html += """
                </table>
            </div>
            """
            
        # Add visualizations if available
        if has_viz:
            html += """
            <div class="metric-group">
                <h2>Visualizations</h2>
            """
            
            viz_files = [f for f in os.listdir(viz_dir) if f.endswith('.png')]
            for viz_file in viz_files:
                title = viz_file.replace('.png', '').replace('_', ' ').title()
                relative_path = f"visualizations/{viz_file}"
                
                html += f"""
                <div class="visualization">
                    <h3>{title}</h3>
                    <img src="{relative_path}" alt="{title}">
                </div>
                """
                
            html += """
            </div>
            """
            
        # Close HTML
        html += """
        </body>
        </html>
        """
        
        return html

# Example usage in AB testing:
"""
metrics = MetricsCollector()

# Record AB test result
metrics.record_ab_test_result(ab_test.summarize_results())

# Record individual conversation metrics during tests
for response_data in ab_test.results["a"]["responses"]:
    metrics.record_conversation_metrics(
        user_input=response_data["prompt"],
        response=response_data["response"],
        anchor_name="<anchor used>",
        sentiment={"label": "POSITIVE", "score": 0.8},  # Get from response data
        times={"total": 0.1},  # Get from response data
        session_id="a_test_session",
        persona_name=response_data["persona"],
        satisfaction_score=response_data["persona_score"]
    )

# Generate and export report
metrics.export_metrics_report()
"""