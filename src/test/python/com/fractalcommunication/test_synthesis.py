import unittest
import sys
import os

# Use relative imports that work with test runner
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../../src/main/python')))

from com.fractalcommunication.synthesis import SynthesisModule
from com.fractalcommunication.state import ConversationState

class TestSynthesisModule(unittest.TestCase):
    def setUp(self):
        self.synthesis_module = SynthesisModule()
    
    def test_synthesize(self):
        reflection = "Test reflection"
        anchored_response = "Test anchored response"
        state = ConversationState("Test user input")
        
        synthesis = self.synthesis_module.synthesize(reflection, anchored_response, state)
        
        # Verify synthesis contains the anchored response
        self.assertIn(anchored_response, synthesis)
        # Verify synthesis has additional content
        self.assertGreater(len(synthesis), len(anchored_response))
        # Verify synthesis contains expected phrases
        self.assertIn("warmth", synthesis)
        self.assertIn("heart", synthesis)
    
    def test_get_synthesis_metrics(self):
        metrics = self.synthesis_module.get_synthesis_metrics()
        self.assertIn("synthesesPerformed", metrics)
        self.assertEqual(metrics["synthesesPerformed"], 1)

if __name__ == '__main__':
    unittest.main()