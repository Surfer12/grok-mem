#!/usr/bin/env python3
"""
Comprehensive test suite for the Fractal Communication Framework

This file contains all unit tests for the FCF components.
Run this file directly to execute all tests.
"""

import unittest
from unittest.mock import Mock, ANY
import sys
import os

# Add the main source directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src/main/python')))

# Import FCF components for testing
from com.fractalcommunication.anchor import ConnectionAnchor, GroundingAnchor, OpennessAnchor
from com.fractalcommunication.anchor_module import AnchorModule
from com.fractalcommunication.interfaces import IAnchor
from com.fractalcommunication.memory import InMemoryMemory, UserProfile
from com.fractalcommunication.metrics import SimpleMetricsLogger
from com.fractalcommunication.orchestrator import Orchestrator
from com.fractalcommunication.reflection import ReflectionEngine
from com.fractalcommunication.state import ConversationState
from com.fractalcommunication.synthesis import SynthesisModule


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