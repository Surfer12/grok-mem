import unittest
from unittest.mock import Mock
import sys
import os

# Use relative imports that work with test runner
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../../src/main/python')))

from com.fractalcommunication.anchor_module import AnchorModule
from com.fractalcommunication.interfaces import IAnchor
from com.fractalcommunication.state import ConversationState

class TestAnchorModule(unittest.TestCase):
    def setUp(self):
        self.anchor_module = AnchorModule()
        
        # Create mock anchors
        self.mock_anchor1 = Mock(spec=IAnchor)
        self.mock_anchor1.name.return_value = "test_anchor1"
        self.mock_anchor1.microtest.return_value = True
        
        self.mock_anchor2 = Mock(spec=IAnchor)
        self.mock_anchor2.name.return_value = "test_anchor2"
        self.mock_anchor2.microtest.return_value = True
    
    def test_register_anchor(self):
        self.anchor_module.register_anchor(self.mock_anchor1)
        self.assertEqual(len(self.anchor_module.get_anchor_names()), 1)
        self.assertIn("test_anchor1", self.anchor_module.get_anchor_names())
        
    def test_select_anchor(self):
        # Register two anchors
        self.anchor_module.register_anchor(self.mock_anchor1)
        self.anchor_module.register_anchor(self.mock_anchor2)
        
        # Create a state with empty history - should select first anchor
        state = ConversationState("test input")
        anchor = self.anchor_module.select_anchor(state)
        self.assertEqual(anchor.name(), "test_anchor1")
        
        # Create a state with one history item - should select second anchor
        state = ConversationState("test input", history=[{"user_input": "previous", "output": "previous output"}])
        anchor = self.anchor_module.select_anchor(state)
        self.assertEqual(anchor.name(), "test_anchor2")
        
    def test_run_microtests(self):
        self.anchor_module.register_anchor(self.mock_anchor1)
        self.anchor_module.register_anchor(self.mock_anchor2)
        
        results = self.anchor_module.run_microtests()
        self.assertTrue(results["test_anchor1"])
        self.assertTrue(results["test_anchor2"])
        
    def test_get_anchor_names(self):
        self.anchor_module.register_anchor(self.mock_anchor1)
        self.anchor_module.register_anchor(self.mock_anchor2)
        
        names = self.anchor_module.get_anchor_names()
        self.assertEqual(len(names), 2)
        self.assertIn("test_anchor1", names)
        self.assertIn("test_anchor2", names)

if __name__ == '__main__':
    unittest.main()