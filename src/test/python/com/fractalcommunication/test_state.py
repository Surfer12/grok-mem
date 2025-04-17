import unittest
import sys
import os

# Use relative imports that work with test runner
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../../src/main/python')))

from com.fractalcommunication.state import ConversationState

class TestConversationState(unittest.TestCase):
    def test_init_with_defaults(self):
        state = ConversationState("Test input")
        self.assertEqual(state.user_input, "Test input")
        self.assertEqual(state.context, {})
        self.assertEqual(state.memory, {})
        self.assertEqual(state.history, [])
        self.assertIsNone(state.session_id)
    
    def test_init_with_custom_values(self):
        context = {"style": "test_style"}
        memory = {"key": "value"}
        history = [{"user_input": "previous", "output": "previous output"}]
        session_id = "test_session"
        
        state = ConversationState(
            "Test input",
            context=context,
            memory=memory,
            history=history,
            session_id=session_id
        )
        
        self.assertEqual(state.user_input, "Test input")
        self.assertEqual(state.context, context)
        self.assertEqual(state.memory, memory)
        self.assertEqual(state.history, history)
        self.assertEqual(state.session_id, session_id)
    
    def test_update_history(self):
        state = ConversationState("Test input")
        entry = {"user_input": "Test input", "output": "Test output"}
        
        # Initial history should be empty
        self.assertEqual(len(state.history), 0)
        
        # Update history
        state.update_history(entry)
        
        # History should now have one entry
        self.assertEqual(len(state.history), 1)
        self.assertEqual(state.history[0], entry)
        
        # Update history again
        entry2 = {"user_input": "Next input", "output": "Next output"}
        state.update_history(entry2)
        
        # History should now have two entries in order
        self.assertEqual(len(state.history), 2)
        self.assertEqual(state.history[0], entry)
        self.assertEqual(state.history[1], entry2)

if __name__ == '__main__':
    unittest.main()