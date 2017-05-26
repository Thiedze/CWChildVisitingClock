from effect import Effect
from datetime import datetime, timedelta

from clockobject import ClockObject

import configparser

import random
'''
The clock effect class.
'''
class ClockEffect(Effect):

	def __init__(self, drawing):
		Effect.__init__(self, drawing)
		
		config = configparser.ConfigParser()
		config.read('cwchildvisitingclock.properties')

		self.toGoColor = map(int, config['DEFAULT']['toGoColor'].split(','))
		self.fromGoColor = map(int, config['DEFAULT']['toFromColor'].split(','))
		self.beatColor = map(int, config['DEFAULT']['beatColor'].split(','))

		self.visitTime = datetime.strptime(config['DEFAULT']['visitTime'], '%H:%M:%S') 

		self.isAcceptanceModeOn = config.getboolean('DEFAULT', 'isAcceptanceModeOn')

	'''
	Reset the clock plan. 
	'''
	def resetPlan(self, plan):
		for index in range(60):
			plan[index] = None

	'''
	Add the beat objects to the plan.
	'''
	def addBeatObjects(self, beat, plan):	
		plan[beat] = ClockObject(self.beatColor)

	'''
	Add the objects "to go" to the finish to the plan. 
	'''
	def addToGoObjects(self, toGo, plan):
		for led in range(0, toGo):
			plan[led] = ClockObject(self.toGoColor)

	def addFromGoObjects(self, fromGo, plan):
		for led in range(fromGo, 60):
			plan[led] = ClockObject(self.fromGoColor)
	'''
	Show the clock effect.
	'''
	def show(self, plan):
		self.resetPlan(plan)
		currentTime = datetime.now()

		if self.isAcceptanceModeOn == True:
			minutesToGo = self.visitTime.minute - currentTime.minute 
			print('minutesToGo: ' ,minutesToGo)
			if(minutesToGo <= 12 and minutesToGo > 0):
				print(currentTime)
				self.addBeatObjects(currentTime.second, plan)
				self.addToGoObjects(minutesToGo, plan)
		else:
			if currentTime > self.visitTime - timedelta(hours = 12):
				hoursToGo = self.visitTime.hour - currentTime.hour 
				if(hoursToGo <= 12 and hoursToGo > 0):
					self.addFromGoObjects(currentTime.minute, plan)
					self.addToGoObjects(hoursToGo, plan)
					self.addBeatObjects(currentTime.second, plan)

		self.drawing.clockPlan(plan)
