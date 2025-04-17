import unittest
import sys
import os

# Use relative imports that work with test runner
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../../src/main/python')))

from com.fractalcommunication.metrics import SimpleMetricsLogger
from com.fractalcommunication.state import ConversationState

class TestSimpleMetricsLogger(unittest.TestCase):
    def setUp(self):
        self.metrics_logger = SimpleMetricsLogger()
        self.test_state = ConversationState("test input")
        
    def test_log_reflection(self):
        self.metrics_logger.log_reflection(self.test_state, "Test reflection text")
        # Check metrics were recorded
        self.assertIn("ReflectionEngine_reflectionLength", self.metrics_logger.metrics)
        values = self.metrics_logger.metrics["ReflectionEngine_reflectionLength"]
        self.assertEqual(values[-1], len("Test reflection text"))
        
    def test_log_anchor(self):
        self.metrics_logger.log_anchor("test_anchor", True, self.test_state)
        self.assertIn("AnchorModule_anchorApplicationSuccess", self.metrics_logger.metrics)
        values = self.metrics_logger.metrics["AnchorModule_anchorApplicationSuccess"]
        self.assertEqual(values[-1], "test_anchor")
        
        # Test failed anchor
        self.metrics_logger.log_anchor("failed_anchor", False, self.test_state)
        values = self.metrics_logger.metrics["AnchorModule_anchorApplicationSuccess"]
        self.assertEqual(values[-1], "FAILED")
        
    def test_log_outcome(self):
        self.metrics_logger.log_outcome(self.test_state, "Test outcome text")
        self.assertIn("SynthesisModule_outputLength", self.metrics_logger.metrics)
        values = self.metrics_logger.metrics["SynthesisModule_outputLength"]
        self.assertEqual(values[-1], len("Test outcome text"))
        
    def test_log_error(self):
        self.metrics_logger.log_error("TestModule", "Test error message")
        self.assertIn("TestModule", self.metrics_logger.errors)
        values = self.metrics_logger.errors["TestModule"]
        self.assertEqual(values[-1], "Test error message")
        
        # Test with cause
        cause = Exception("Test cause")
        self.metrics_logger.log_error("TestModule", "Error with cause", cause)
        values = self.metrics_logger.errors["TestModule"]
        self.assertIn("Error with cause", values[-1])
        self.assertIn("Test cause", values[-1])
        
    def test_get_all_metrics(self):
        # Add some test metrics
        self.metrics_logger.log_reflection(self.test_state, "Test reflection")
        self.metrics_logger.log_anchor("test_anchor", True, self.test_state)
        self.metrics_logger.log_error("TestModule", "Test error")
        
        all_metrics = self.metrics_logger.get_all_metrics()
        self.assertIn("ReflectionEngine_reflectionLength_count", all_metrics)
        self.assertEqual(all_metrics["ReflectionEngine_reflectionLength_count"], 1)
        self.assertIn("AnchorModule_anchorApplicationSuccess_count", all_metrics)
        self.assertEqual(all_metrics["AnchorModule_anchorApplicationSuccess_count"], 1)
        self.assertIn("TestModule_error_count", all_metrics)
        self.assertEqual(all_metrics["TestModule_error_count"], 1)

if __name__ == '__main__':
    unittest.main()