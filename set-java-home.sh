#!/bin/bash

# Script to set JAVA_HOME and run Magic tasks with Temurin 23 JDK

 echo "Setting JAVA_HOME to Temurin 23 JDK..."
 export JAVA_HOME=/Library/Java/JavaVirtualMachines/temurin-23.jdk/Contents/Home
 echo "JAVA_HOME set to: $JAVA_HOME"

# Check if a task is provided as an argument
 if [ $# -eq 0 ]; then
     echo "No task provided. Running 'magic run java-all-tests' by default."
     magic run java-all-tests
 else
     echo "Running Magic task: $@"
     magic run "$@"
 fi
