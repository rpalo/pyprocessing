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
		self.linecolor = "black"
		self.fill = "white"

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

	def rect(self, x, y, width, height, **kwargs):
		"""Draws a rectangle with top-left corner at x, y.  Returns id
		of object"""

		return self.canvas.create_rectangle(x, y, x + width, y + height, **kwargs)

	def oval(self, x, y, width, height, **kwargs):
		"""Draws an oval with top-left corner at x, y.  Returns id of object"""

		return self.canvas.create_oval(x, y, x + width, y + height, **kwargs)

	def circle(self, x, y, r, **kwargs):
		"""Draws a circle (width = height) with center at x, y.  Returns
		id of object"""

		return self.canvas.create_oval(x - r, y - r, x + r, y + r, **kwargs)

	def clear(self):
		"""Clears the whole canvas out"""
		self.canvas.delete("all")

	def background(self, color):
		"""Sets the background color of the canvas"""
		self.canvas.configure(background=color)


	def mainloop(self):
		"""Runs the mainloop of the animation"""

		self.setup()
		self.root.after(0, self._animate)
		self.root.mainloop()

