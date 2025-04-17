#!/usr/bin/env python3
import unittest
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))

# Import all test modules
from com.fractalcommunication.test_anchor import TestAnchors
from com.fractalcommunication.test_anchor_module import TestAnchorModule
from com.fractalcommunication.test_memory import TestInMemoryMemory, TestUserProfile
from com.fractalcommunication.test_metrics import TestSimpleMetricsLogger
from com.fractalcommunication.test_orchestrator import TestOrchestrator
from com.fractalcommunication.test_reflection import TestReflectionEngine
from com.fractalcommunication.test_state import TestConversationState
from com.fractalcommunication.test_synthesis import TestSynthesisModule

def run_tests():
    # Create a test suite
    test_suite = unittest.TestSuite()
    
    # Add all test cases
    test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestAnchors))
    test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestAnchorModule))
    test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestInMemoryMemory))
    test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestUserProfile))
    test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestSimpleMetricsLogger))
    test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestOrchestrator))
    test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestReflectionEngine))
    test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestConversationState))
    test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestSynthesisModule))
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Return appropriate exit code
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    sys.exit(run_tests())