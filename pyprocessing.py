import tkinter as tk
from math import sin, asin, cos, acos, tan, atan2, radians, degrees, pi, sqrt

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
			"fill": "",
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
		"""Main animation mechanics for draw loop"""
		try:
			self.draw()
		except NotImplementedError:
			return False
		self.root.after(self.timestep, self._animate)
		self.frame += 1

	def _toGlobal(self, x_local, y_local):
		"""Converts local x, y to global x, y.
		Returns tuple of pixel coords."""
		theta = radians(self.matrix["rotation"])
		x_global = self.matrix["origin_x"] + x_local*cos(theta) + y_local*sin(theta)
		y_global = self.matrix["origin_y"] + y_local*cos(theta) - x_local*sin(theta)
		return x_global, y_global


	def rect(self, x, y, width, height):
		"""Draws a rectangle with top-left corner at x, y.  Returns id
		of object"""

		local_points = [(x, y), (x+width, y), (x+width, y+height), (x, y+height)]
		global_points = []
		for _x, _y in local_points:
			global_points.append(self._toGlobal(_x, _y))

		return self.canvas.create_polygon(
								outline=self.matrix["linecolor"],
								fill=self.matrix["fill"],
								width=self.matrix["linewidth"],
								*global_points)

	def oval(self, x, y, width, height, resolution=20):
		"""Draws an oval with top-left corner at x, y.  Returns id of object"""
		global_points = []
		theta = 0
		theta_step = 2*pi/resolution
		a = width/2
		b = height/2
		xc = x + a
		yc = y + b
		for i in range(resolution):
			theta = theta + theta_step
			x1 = a*cos(theta) + xc 
			y1 = b*sin(theta) + yc 
			global_points.append(self._toGlobal(x1, y1))

		return self.canvas.create_polygon(
								outline=self.matrix["linecolor"],
								fill=self.matrix["fill"],
								width=self.matrix["linewidth"],
								*global_points)

	def circle(self, x, y, r, resolution=20):
		"""Draws a circle (width = height) with center at x, y.  Returns
		id of object"""
		return self.oval(x-r, y-r, 2*r, 2*r, resolution)

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
		self.matrixStack.append(self.matrix.copy())

	def popMatrix(self):
		"""Pops a matrix off of the stack, restoring those settings"""
		self.matrix = self.matrixStack.pop()

	def translate(self, x, y):
		"""Translates the origin to a proscribed x, y point"""
		self.matrix["origin_x"] += x 
		self.matrix["origin_y"] += y

	def rotate(self, theta):
		"""Rotates the origin reference frame by theta degrees.
		Theta zero is positive x axis, positive theta is ccw"""
		self.matrix["rotation"] = theta

	def stroke(self, **kwargs):
		"""Takes in some stroke variables and sets them.  Possible inputs:
		width = sets the line width
		color = sets the pen color"""
		if "width" in kwargs:
			self.matrix["linewidth"] = kwargs["width"]
		if "color" in kwargs:
			self.matrix["linecolor"] = kwargs["color"]

	def mainloop(self):
		"""Runs the mainloop of the animation"""

		self.setup()
		self.root.after(0, self._animate)
		self.root.mainloop()

class PVector:
	"""Python implementation of Processing's PVector class, which is
	(until I learn differently), basically a vector.  One might call
	this one a... PYVector.  Heh.  Essentially it has an x and y component
	which can be converted back and forth to angle and magnitude. 
	Various supporting mathematical functions ensue.  I know that
	there is most definitely already a python implementation of a vector
	out there and that it is probably way better than this, but
	I'm making this one for fun."""

	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __str__(self):
		return "<%f, %f>" % (self.x, self.y)

	def __repr__(self):
		return "<PVector: (%f, %f)>" % (self.x, self.y)

	def __add__(self, other):
		if isinstance(other, PVector):
			return PVector(self.x + other.x, self.y + other.y)
		else:
			return PVector(self.x + other,self.y + other)

	def __sub__(self, other):
		if isinstance(other, PVector):
			return PVector(self.x - other.x, self.y - other.y)
		else:
			return PVector(self.x - other, self.y - other)

	def __mul__(self, other):
		if isinstance(other, PVector):
			return self.dot(other)
		else:
			return PVector(self.x * other, self.y * other)

	def __div__(self, other):
		return PVector(self.x / other, self.y / other)

	def __neg__(self, other):
		return PVector(-self.x, -self.y)

	def cross(self, other):
		"""Returns the cross product of self and other. 
		Obviously since these are all 2D, cross product will
		be in Z dimension only.  Return value is a floating
		point number, in the k dimension"""

		return (self.x * other.y) - (self.y * other.x)

	def dot(self, other):
		"""Returns the dot product of self and other"""

		return self.x * other.x + self.y * other.y

	def mag(self):
		"""Returns the vectors magnitude"""
		return sqrt(self.x**2 + self.y**2)

	def theta(self, degree=True):
		"""Returns the vector's angle"""
		if degree:
			return degrees(atan2(self.y, self.x))
		else:
			return atan2(self.y, self.x)

	def setMag(self, magnitude):
		"""Sets this vectors magnitude at same angle"""
		mag = self.mag()
		theta = self.theta(degree=False)
		self.x = magnitude*cos(theta)
		self.y = magnitude*sin(theta)

	def scale(self, factor):
		"""Scales this vector's magnitude by a certain factor
		while keeping the angle the same."""

		self.setMag(factor*self.mag())

	def norm(self):
		"""Scales self to unit vector"""
		self.setMag(1)

	def rotate(self, angle):
		"""Rotates vector by angle degrees.  Positive theta ccw"""
		theta = self.theta(degree=False)
		theta += radians(angle)
		mag = self.mag()
		self.x = mag*cos(theta)
		self.y = mag*sin(theta)

	def get_angle_between(self, other):
		return degrees(acos(self.dot(other)/(self.mag()*other.mag())))

