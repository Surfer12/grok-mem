#!/usr/bin/env python3
# Fractal Communication Framework Demo Runner

import sys
import os

# Add the src/main/python directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from com.fractalcommunication.demo import main

if __name__ == "__main__":
    main()