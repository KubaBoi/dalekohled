#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Cheese.cheese import CheeseBurger

from src.tools.camera import *
from src.tools.streamingOutput import *

"""
File generated by Cheese Framework

main file of Cheese Application
"""

if __name__ == "__main__":
    CheeseBurger.init()

    StreamingOutput.init()
    Camera.init()
    Camera.start_recording()

    try:
        CheeseBurger.serveForever()
    finally:
        Camera.stop_recording()