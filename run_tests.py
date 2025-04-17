#!/usr/bin/env python3
"""
Test runner for the Fractal Communication Framework

This script runs all the unit tests for the FCF framework.
It handles the Python path setup automatically.
"""

import unittest
import sys
import os

# Add the necessary paths for imports to work
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src/main/python')))

# Import test modules
from src.test.python.com.fractalcommunication.test_anchor import TestAnchors
from src.test.python.com.fractalcommunication.test_anchor_module import TestAnchorModule
from src.test.python.com.fractalcommunication.test_memory import TestInMemoryMemory, TestUserProfile
from src.test.python.com.fractalcommunication.test_metrics import TestSimpleMetricsLogger
from src.test.python.com.fractalcommunication.test_orchestrator import TestOrchestrator
from src.test.python.com.fractalcommunication.test_reflection import TestReflectionEngine
from src.test.python.com.fractalcommunication.test_state import TestConversationState
from src.test.python.com.fractalcommunication.test_synthesis import TestSynthesisModule

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