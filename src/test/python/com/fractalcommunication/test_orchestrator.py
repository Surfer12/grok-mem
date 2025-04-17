import unittest
from unittest.mock import Mock, ANY
import sys
import os

# Use relative imports that work with test runner
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../../src/main/python')))

from com.fractalcommunication.orchestrator import Orchestrator
from com.fractalcommunication.interfaces import IAnchor
from com.fractalcommunication.state import ConversationState

class TestOrchestrator(unittest.TestCase):
    def setUp(self):
        # Create mocks for all dependencies
        self.mock_reflection_engine = Mock()
        self.mock_reflection_engine.reflect.return_value = "Mock reflection"
        
        self.mock_anchor = Mock(spec=IAnchor)
        self.mock_anchor.name.return_value = "mock_anchor"
        self.mock_anchor.apply.return_value = "Mock anchored response"
        self.mock_anchor.microtest.return_value = True
        
        self.mock_anchor_module = Mock()
        self.mock_anchor_module.select_anchor.return_value = self.mock_anchor
        
        self.mock_synthesis_module = Mock()
        self.mock_synthesis_module.synthesize.return_value = "Mock synthesized output"
        
        self.mock_memory = Mock()
        self.mock_memory.get_short_term.return_value = {}
        
        self.mock_metrics_logger = Mock()
        
        # Create orchestrator with mocks
        self.orchestrator = Orchestrator(
            reflection_engine=self.mock_reflection_engine,
            anchor_module=self.mock_anchor_module,
            synthesis_module=self.mock_synthesis_module,
            memory=self.mock_memory,
            metrics_logger=self.mock_metrics_logger
        )
    
    def test_run_conversation_success_path(self):
        # Test the happy path
        result = self.orchestrator.run_conversation("Test input", "test_user", "test_session")
        
        # Verify all methods were called with expected parameters
        self.mock_reflection_engine.reflect.assert_called_once()
        self.mock_anchor_module.select_anchor.assert_called_once()
        self.mock_anchor.apply.assert_called_once_with("Mock reflection", ANY)
        self.mock_synthesis_module.synthesize.assert_called_once()
        
        # Verify metrics were logged
        self.mock_metrics_logger.log_reflection.assert_called_once()
        self.mock_metrics_logger.log_anchor.assert_called_once_with("mock_anchor", True, ANY)
        self.mock_metrics_logger.log_outcome.assert_called_once()
        
        # Verify memory was updated
        self.mock_memory.update.assert_called_once()
        
        # Verify correct result
        self.assertEqual(result, "Mock synthesized output")
    
    def test_run_conversation_no_anchor(self):
        # Test when no anchor is available
        self.mock_anchor_module.select_anchor.return_value = None
        
        result = self.orchestrator.run_conversation("Test input", "test_user")
        
        # Verify error was handled
        self.mock_metrics_logger.log_error.assert_called_once()
        self.assertEqual(result, "I'm having trouble processing that. Could you clarify what you mean?")
    
    def test_handle_error(self):
        state = ConversationState("test input")
        error = Exception("Test error")
        result = self.orchestrator.handle_error(error, state)
        self.assertEqual(result, "I'm having trouble processing that. Could you clarify what you mean?")
    
    def test_branch(self):
        state = ConversationState("test input", session_id="test_session")
        options = ["Option 1", "Option 2", "Option 3"]
        result = self.orchestrator.branch(state, options)
        
        # Verify options were stored
        self.assertIn("test_session", self.orchestrator.active_branches)
        self.assertIn(options, self.orchestrator.active_branches["test_session"])
        
        # Verify correct response format
        self.assertIn("Option 1", result)
        self.assertIn("Option 2", result)
        self.assertIn("Option 3", result)
    
    def test_interrupt(self):
        state = ConversationState("test input", session_id="test_session")
        reason = "urgent issue"
        result = self.orchestrator.interrupt(state, reason)
        
        # Verify interruption was logged
        self.mock_metrics_logger.log_error.assert_called_once_with("Orchestrator", f"Interruption: {reason}")
        
        # Verify correct response format
        self.assertIn(reason, result)

if __name__ == '__main__':
    unittest.main()