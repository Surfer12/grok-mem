import unittest
import sys
import os

# Use relative imports that work with test runner
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../../src/main/python')))

from com.fractalcommunication.memory import InMemoryMemory, UserProfile

class TestInMemoryMemory(unittest.TestCase):
    def setUp(self):
        self.memory = InMemoryMemory()
        
    def test_short_term_memory(self):
        self.memory.update("test_key", "test_value", scope="short_term")
        short_term = self.memory.get_short_term()
        self.assertIn("test_key", short_term)
        self.assertEqual(short_term["test_key"], "test_value")
        
    def test_long_term_memory(self):
        self.memory.update("test_key", "test_value", scope="long_term")
        long_term = self.memory.get_long_term()
        self.assertIn("test_key", long_term)
        self.assertEqual(long_term["test_key"], "test_value")
        
    def test_session_memory(self):
        session_id = "test_session"
        self.memory.update("test_key", "test_value", scope="session", session_id=session_id)
        session = self.memory.get_session(session_id)
        self.assertIn("test_key", session)
        self.assertEqual(session["test_key"], "test_value")
        
    def test_get_session_creates_new_session(self):
        session_id = "new_session"
        # This should create a new session
        session = self.memory.get_session(session_id)
        self.assertEqual(session, {})
        
class TestUserProfile(unittest.TestCase):
    def test_create_user_profile_with_defaults(self):
        user_id = "test_user"
        profile = UserProfile(user_id)
        self.assertEqual(profile.user_id, user_id)
        self.assertEqual(profile.interaction_style, {"style": "fractal"})
        self.assertEqual(profile.preferred_anchors, ["connection"])
        
    def test_create_user_profile_with_custom_values(self):
        user_id = "test_user"
        style = {"style": "direct", "tone": "formal"}
        anchors = ["grounding", "openness"]
        profile = UserProfile(user_id, style, anchors)
        self.assertEqual(profile.user_id, user_id)
        self.assertEqual(profile.interaction_style, style)
        self.assertEqual(profile.preferred_anchors, anchors)
        
    def test_update_interaction_style(self):
        profile = UserProfile("test_user")
        profile.update_interaction_style({"tone": "casual"})
        self.assertIn("tone", profile.interaction_style)
        self.assertEqual(profile.interaction_style["tone"], "casual")
        self.assertEqual(profile.interaction_style["style"], "fractal")

if __name__ == '__main__':
    unittest.main()