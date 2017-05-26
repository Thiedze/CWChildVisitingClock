from threading import Timer
from repeatedtimer import RepeatedTimer

from drawing import Drawing

from clockeffect import ClockEffect

'''
The clock class. This is the main class to control the effects. 
'''
class Clock():

	'''
	Init the clock object.
	'''
	def __init__(self):
		self.programm = None
		
		self.drawing = Drawing()
		self.clockEffect = ClockEffect(self.drawing)
	'''
	Draw a clear plan.
	'''
	def clear(self):
		self.drawing.clear()

	'''
	Get a new plan
	'''
	def getNewPlan(self):
		plan = list()
		for _ in range(60):
			plan.append(None)
		return plan

	'''
	Start a timer. If any other timer exist stop it first. 
	'''
	def startTimer(self, time, function):
		if(self.programm != None):
			self.programm.stop()
		self.programm = RepeatedTimer(time, function, self.getNewPlan())

	'''
	Run clock
	'''
	def run(self, mode = None, showSingleEffect = None):	
		self.startTimer(0.25, self.clockEffect.show)


