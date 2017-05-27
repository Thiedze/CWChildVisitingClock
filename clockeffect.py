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
		
		self.config = configparser.ConfigParser()
		self.config.read('cwchildvisitingclock.properties')
		self.isAcceptanceModeOn = self.config.getboolean('DEFAULT', 'isAcceptanceModeOn')

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
		for led in range(60 - fromGo, 60):
			plan[led] = ClockObject(self.fromGoColor)
	'''
	Show the clock effect.
	'''
	def show(self, plan):
		self.resetPlan(plan)
		currentTime = datetime.now()
		self.config.read('cwchildvisitingclock.properties')
		visitTime = datetime.strptime(self.config['DEFAULT']['visitTime'], '%H:%M:%S') 
		self.toGoColor = map(int, self.config['DEFAULT']['toGoColor'].split(','))
		self.fromGoColor = map(int, self.config['DEFAULT']['toFromColor'].split(','))
		self.beatColor = map(int, self.config['DEFAULT']['beatColor'].split(','))

		if self.isAcceptanceModeOn == True:
			minutesToGo = visitTime.minute - currentTime.minute 
			if(minutesToGo <= 12 and minutesToGo > 0):
				self.addBeatObjects(currentTime.second, plan)
				self.addToGoObjects(minutesToGo, plan)
		else:
			hoursToGo = visitTime.hour - currentTime.hour 
			minutesToGo = visitTime.minute - currentTime.minute
			if (hoursToGo == 0 and minutesToGo > 0) or (hoursToGo >= 1 and hoursToGo < 12):
				self.addFromGoObjects(minutesToGo, plan)
				self.addToGoObjects(hoursToGo, plan)
				self.addBeatObjects(currentTime.second, plan)

		self.drawing.clockPlan(plan)
