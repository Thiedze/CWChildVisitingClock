#!/bin/sh

'''
Child Visiting Clock 

Run this script to start the clock. 

Programmed by Sebastian Thiems

May 2017
'''
from clock import Clock
import time

'''
Start the drawing.
'''
clock = Clock()
clock.clear()
time.sleep(2)
clock.run()
