#!/bin/sh

'''
Child Visiting Clock 

Run this script to start the clock. 

Programmed by Sebastian Thiems

May 2017
'''
from clock import Clock
import time
from BaseHTTPServer import HTTPServer

from httphandler import HttpHandler

'''
Start the drawing.
'''
#time.sleep(60)
clock = Clock()
clock.clear()
clock.run()

try:
	server = HTTPServer(('', 8080), HttpHandler)
	server.serve_forever()
except KeyboardInterrupt:
	server.socket.close()
