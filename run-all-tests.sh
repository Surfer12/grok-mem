#!/bin/bash

# Script to run all tests (unit tests and micro-tests) for the Fractal Communication Framework

 echo "Running all tests for Fractal Communication Framework..."

# Run Maven unit tests
 echo "Running Maven unit tests..."
 mvn clean test
 if [ $? -ne 0 ]; then
     echo "Maven unit tests failed. Check output for details."
     exit 1
 fi

# Run micro-tests for anchors
 echo "Running micro-tests for anchors..."
 ./run-micro-tests.sh
 if [ $? -ne 0 ]; then
     echo "Micro-tests failed. Check output for details."
     exit 1
 fi

 echo "All tests completed successfully."
