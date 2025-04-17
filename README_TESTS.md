# Fractal Communication Framework - Unit Tests

## Overview

This document provides information about the unit tests created for the Fractal Communication Framework (FCF).

## Test Structure

The unit tests are organized in the following structure:

```
grok-mem/
├── src/
│   ├── main/python/    # Main source code
│   └── test/python/    # Test files
│       └── com/fractalcommunication/
│           ├── test_anchor.py         # Tests for anchor classes
│           ├── test_anchor_module.py  # Tests for anchor module
│           ├── test_memory.py         # Tests for memory classes
│           ├── test_metrics.py        # Tests for metrics logger
│           ├── test_orchestrator.py   # Tests for orchestrator
│           ├── test_reflection.py     # Tests for reflection engine
│           ├── test_state.py          # Tests for conversation state
│           └── test_synthesis.py      # Tests for synthesis module
└── run_tests.py       # Test runner script
```

## Running the Tests

To run all tests, execute the following command from the project root:

```bash
python run_tests.py
```

Or with Python 3 explicitly:

```bash
python3 run_tests.py
```

## Test Coverage

The tests cover the following components of the FCF:

1. **Anchors**: Testing the three anchor implementations (Connection, Grounding, Openness)
2. **Anchor Module**: Testing anchor registration, selection, and microtests
3. **Memory**: Testing the in-memory storage and user profiles
4. **Metrics**: Testing the metrics logging functionality
5. **Orchestrator**: Testing the main conversation flow and error handling
6. **Reflection**: Testing the reflection generation
7. **State**: Testing the conversation state management
8. **Synthesis**: Testing the output synthesis

## Individual Test Execution

To run individual test files, you can use Python's unittest module directly:

```bash
python -m unittest src.test.python.com.fractalcommunication.test_anchor
```

## Adding New Tests

When adding new tests, follow these guidelines:

1. Create test files with the `test_` prefix
2. Use the unittest framework
3. Ensure each test method name starts with `test_`
4. Use appropriate assertions for validation

## Mocking

The tests use Python's unittest.mock for mocking dependencies and isolating components for testing.