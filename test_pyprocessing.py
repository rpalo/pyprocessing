import pyprocessing as proc 

class TestPlot(proc.Plotter):

	def setup(self):
		"""Adds a test setup method"""

		self.rect(self.width/2, self.height/2, 100, 20)

	def draw(self):
		"""Adds a test draw method"""

		self.clear()
		self.circle(self.width/2 + self.frame*10, self.height/2, 20, fill="black")

if __name__ == '__main__':
	t = TestPlot()
	t.mainloop()