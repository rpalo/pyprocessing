import tkinter as tk 

class Plotter:
	"""Main controller class.  Basically simulates a processing
	window and provides the interfaces to the tkinter inner workings.
	Not sure if this is the best way to go on this yet."""

	def __init__(self, width=600, height=600, timestep=100):
		self.root = tk.Tk()
		self.width = width
		self.height = height
		self.timestep = timestep
		self.canvas = tk.Canvas(self.root,
								width=self.width,
								height=self.height)
		self.canvas.pack()
		self.frame = 0
		self.matrix = {
			"linecolor": "black",
			"fill": "white",
			"origin_x": 0,
			"origin_y": 0,
			"rotation": 0,
			"linewidth": 2,
		}
		self.matrixStack = []

	def setup(self):
		"""Sets up the window before the first frame goes.
		To be implemented in all subclasses"""
		
		raise NotImplementedError("Setup method was not set")

	def draw(self):
		"""This function to be run once per frame, drives the animation.
		To be implemented in all subclasses.  If it isn't, animation will
		stop"""

		raise NotImplementedError("Draw method was not set")

	def _animate(self):
		try:
			self.draw()
		except NotImplementedError:
			return False
		self.root.after(self.timestep, self._animate)
		self.frame += 1

	def rect(self, x, y, width, height):
		"""Draws a rectangle with top-left corner at x, y.  Returns id
		of object"""

		x0 = x + self.matrix["origin_x"]
		y0 = y + self.matrix["origin_y"]
		x1 = x0 + width
		y1 = y0 + width
		return self.canvas.create_rectangle(x0, y0, x1, y1,
								outline=self.matrix["linecolor"],
								fill=self.matrix["fill"],
								width=self.matrix["linewidth"])

	def oval(self, x, y, width, height):
		"""Draws an oval with top-left corner at x, y.  Returns id of object"""

		x0 = x + self.matrix["origin_x"]
		y0 = y + self.matrix["origin_y"]
		x1 = x0 + width
		y1 = y0 + height
		return self.canvas.create_oval(x0, y0, x1, y1,
								outline=self.matrix["linecolor"],
								fill=self.matrix["fill"],
								width=self.matrix["linewidth"])

	def circle(self, x, y, r):
		"""Draws a circle (width = height) with center at x, y.  Returns
		id of object"""

		x0 = x + self.matrix["origin_x"] - r 
		y0 = y + self.matrix["origin_y"] - r 
		x1 = x0 + 2*r 
		y1 = y0 + 2*r

		return self.canvas.create_oval(x0, y0, x1, y1,
								outline=self.matrix["linecolor"],
								fill=self.matrix["fill"],
								width=self.matrix["linewidth"])

	def clear(self):
		"""Clears the whole canvas out"""
		self.canvas.delete("all")

	def background(self, color):
		"""Sets the background color of the canvas"""
		self.canvas.configure(background=color)

	def fill(self, color):
		"""Sets the active fill to the current color"""
		self.matrix["fill"] = color

	def pushMatrix(self):
		"""Saves the current major settings for unpacking later"""
		self.matrixStack.append(self.matrix)

	def popMatrix(self):
		"""Pops a matrix off of the stack, restoring those settings"""
		self.matrix = self.matrixStack.pop()

	def translate(self, x, y):
		"""Translates the origin to a proscribed x, y point"""
		self.matrix["origin_x"] = x 
		self.matrix["origin_y"] = y

	def mainloop(self):
		"""Runs the mainloop of the animation"""

		self.setup()
		self.root.after(0, self._animate)
		self.root.mainloop()

