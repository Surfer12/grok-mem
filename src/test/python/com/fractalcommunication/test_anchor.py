import unittest
import sys
import os

# Use relative imports that work with test runner
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../../src/main/python')))

from com.fractalcommunication.anchor import ConnectionAnchor, GroundingAnchor, OpennessAnchor

class TestAnchors(unittest.TestCase):
    def test_connection_anchor(self):
        anchor = ConnectionAnchor()
        self.assertEqual(anchor.name(), "connection")
        result = anchor.apply("Test reflection", None)
        self.assertIn("warmth", result)
        self.assertIn("understanding", result)
        self.assertTrue(anchor.microtest())
    
    def test_grounding_anchor(self):
        anchor = GroundingAnchor()
        self.assertEqual(anchor.name(), "grounding")
        result = anchor.apply("Test reflection", None)
        self.assertIn("grounding breath", result)
        self.assertTrue(anchor.microtest())
    
    def test_openness_anchor(self):
        anchor = OpennessAnchor()
        self.assertEqual(anchor.name(), "openness")
        result = anchor.apply("Test reflection", None)
        self.assertIn("curiosity", result)
        self.assertIn("judgment", result)
        self.assertTrue(anchor.microtest())

if __name__ == '__main__':
    unittest.main()