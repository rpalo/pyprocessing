from pyprocessing import Plotter
import sys

"""This module is just an example use case for pyprocessing.
It generates a 1-dimensional Cellular Automaton animation.
Check out rule 90, and several in the 100-120 range."""


class CA:

	def __init__(self, plot, resolution=10, rule=90):
		self.cells = []
		self.ruleset = self.get_ruleset(rule)
		self.resolution = resolution
		self.plot = plot
		for i in range(int(self.plot.width/self.resolution)):
			self.cells.append(0)
		self.cells[int(len(self.cells)/2)] = 1
		self.generation = 0

	def generate(self):
		nextgen = []
		nextgen.append(0)
		for i in range(1, len(self.cells)-1):
			left = self.cells[i-1]
			me = self.cells[i]
			right = self.cells[i+1]
			nextgen.append(self.rules(left, me, right))
		nextgen.append(0)
		self.cells = nextgen
		self.generation += 1

	def rules(self, a, b, c):
		s = "%d%d%d" % (a, b, c)
		index = int(s, 2)
		return self.ruleset[index]

	def display_row(self):
		for i in range(len(self.cells)):
			if self.cells[i] == 1:
				self.plot.fill('black')
			else:
				self.plot.fill('white')
			self.plot.rect(i*self.resolution,
							self.generation*self.resolution,
							self.resolution,
							self.resolution)

	def get_ruleset(self, rule):
		ruleset = [int(x) for x in bin(rule)[2:]]
		while len(ruleset) < 8:
			ruleset.insert(0, 0)
		return ruleset

class CAPlot(Plotter):

	def setup(self):
		self.CA.display_row()

	def draw(self):
		self.CA.generate()
		self.CA.display_row()



if __name__ == '__main__':
	p = CAPlot()
	if len(sys.argv) > 1:
		ca = CA(plot=p, rule=int(sys.argv[1]))
	else:
		ca = CA(plot=p)
	p.CA = ca
	p.mainloop()

