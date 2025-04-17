# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build/Lint/Test Commands
- Java build: `mvn -B clean package` or `pixi run java-build`
- Java lint: `mvn -B checkstyle:check` or `pixi run java-lint`
- Java format: `mvn spotless:apply` or `pixi run java-format`
- Java test: `mvn -B test` or `pixi run java-test`
- Java single test: `mvn -B test -Dtest=TestClassName#testMethodName`
- Python run: `python src/main/python/fcf_demo_runner.py` or `pixi run run-demo`
- Python tests: `python run_tests.py` or `python tests.py`
- Python single test: `python -m unittest src.test.python.com.fractalcommunication.test_module.TestClass.test_method`

## Code Style Guidelines
- Java: JDK 23, camelCase methods/variables, PascalCase classes
- Java interfaces: Prefix with "I" (IMemoryModule)
- Python: >=3.8, snake_case methods/variables, PascalCase classes
- Typing: Full type annotations for all functions
- Formatting: Maven formatter for Java, PEP 8 for Python
- Error handling: Custom FCFException hierarchy in Java, specific exception types in Python
- Tests: JUnit 5 for Java (with Mockito), unittest for Python
- Documentation: Javadoc for Java, docstrings for Python
- Imports: Package-based for Java, absolute imports for Python with explicit typing