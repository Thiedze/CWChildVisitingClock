from effect import Effect
from datetime import datetime, date, timedelta

from clockobject import ClockObject

import configparser

import random
'''
The clock effect class.
'''
class ClockEffect(Effect):

	'''
	Init:
		- the effect
		- acceptence mode from configuration file
	'''
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
	Add the hours to the plan. 
	'''
	def addHourObjects(self, hoursToGo, plan):
		overlayCount = 59 - self.minutesToGo
		for led in range(0, hoursToGo):
			if led > overlayCount and overlayCount < hoursToGo:
				plan[led] = ClockObject([abs(self.hourColor[0] - self.minuteColor[0]), abs(self.hourColor[1] - self.minuteColor[1]), abs(self.hourColor[2] - self.minuteColor[2])])
			else:
				plan[led] = ClockObject(self.hourColor)

	'''
	Add the minutes to the plan.
	'''
	def addMinuteObjects(self, minutesToGo, plan):
		for led in range(60 - minutesToGo, 60):
			plan[led] = ClockObject(self.minuteColor)
	
	'''
	Add the seconds to the plan.
	'''
	def addSecondObjects(self, secondsToGo, plan):	
		plan[secondsToGo] = ClockObject(self.secondColor)

	'''
	Load the configuration from file
	'''
	def loadConfiguration(self):
		self.config.read('cwchildvisitingclock.properties')
		self.visitTime = datetime.time(datetime.strptime(self.config['DEFAULT']['visitTime'], '%H:%M:%S') )
		self.hourColor = map(int, self.config['DEFAULT']['hourcolor'].split(','))
		self.minuteColor = map(int, self.config['DEFAULT']['minutecolor'].split(','))
		self.secondColor = map(int, self.config['DEFAULT']['secondColor'].split(','))
		self.startDelay = int(self.config['DEFAULT']['startdelay'])

	'''
	Calculate the duration till visit time.
	'''
	def calculateDuration(self):
		currentTime = datetime.time(datetime.now())
		duration = datetime.combine(datetime.today() + timedelta(days=1) , self.visitTime)  - datetime.combine(datetime.today(), currentTime)
		self.hoursToGo = divmod(duration.seconds, 3600)[0]
		self.minutesToGo = divmod(duration.seconds - (self.hoursToGo * 3600), 60)[0]
		self.secondsToGo = duration.seconds - (self.hoursToGo * 3600) - (self.minutesToGo * 60)
		
	'''
	Show the clock effect.
	'''
	def show(self, plan):
		self.resetPlan(plan)
		self.loadConfiguration()
		self.calculateDuration()

		if self.isAcceptanceModeOn == True:
			if(self.minutesToGo < self.startDelay):
				self.addHourObjects(self.minutesToGo, plan)
				self.addSecondObjects(self.secondsToGo, plan)
		else:
			if (self.hoursToGo < self.startDelay):
				self.addMinuteObjects(self.minutesToGo, plan)
				self.addHourObjects(self.hoursToGo, plan)
				self.addSecondObjects(59  - self.secondsToGo, plan)
			else:
				print(self.hoursToGo, self.minutesToGo, self.secondsToGo)


		self.drawing.clockPlan(plan)
