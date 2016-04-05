import pyprocessing as proc 

class TestPlot(proc.Plotter):

	def setup(self):
		"""Adds a test setup method"""

		d.display()

	def draw(self):
		"""Adds a test draw method"""

		self.clear()
		d.update()
		d.display()


class Dude:
	"""Little autonomous dude for testing"""

	def __init__(self, plot):
		self.x = plot.width/2
		self.y = 0
		self.vx = 0
		self.vy = 1
		self.ay = 1
		self.plot = plot
	
	def update(self):
		"""Updates all of the little dude's properties at each timestep"""
		self.x += self.vx
		self.vy += self.ay
		self.y += self.vy

	def display(self):
		"""Displays the little dude"""
		self.plot.pushMatrix()
		self.plot.translate(self.x, self.y)
		self.plot.fill('yellow')
		self.plot.circle(0, 0, 30)
		self.plot.fill('black')
		self.plot.circle(-10, -10, 5)
		self.plot.circle(10, -10, 5)
		self.plot.rect(-10, 0, 20, 10)
		self.plot.popMatrix()

if __name__ == '__main__':
	t = TestPlot()
	d = Dude(t)
	t.mainloop()