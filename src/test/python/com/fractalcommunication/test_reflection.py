import unittest
import sys
import os

# Use relative imports that work with test runner
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../../src/main/python')))

from com.fractalcommunication.reflection import ReflectionEngine
from com.fractalcommunication.state import ConversationState

class TestReflectionEngine(unittest.TestCase):
    def setUp(self):
        self.reflection_engine = ReflectionEngine()
    
    def test_reflect(self):
        # Test with basic state
        state = ConversationState(user_input="Test user input")
        reflection = self.reflection_engine.reflect(state)
        
        # Verify reflection contains the user input
        self.assertIn("Test user input", reflection)
        # Verify reflection has the expected format
        self.assertIn("You mentioned", reflection)
        self.assertIn("Let's explore", reflection)
    
    def test_get_reflection_metrics(self):
        metrics = self.reflection_engine.get_reflection_metrics()
        self.assertIn("reflectionsPerformed", metrics)
        self.assertEqual(metrics["reflectionsPerformed"], 1)

if __name__ == '__main__':
    unittest.main()