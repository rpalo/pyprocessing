from pyprocessing import Plotter
import random

class Cell:

	def __init__(self, x, y, w, plot,board):
		self.x = x
		self.y = y
		self.w = w
		self.plot = plot 
		self.board = board
		self.state = 0
		self.previous = 0

	def display(self):
		if self.previous == 0 and self.state == 1:
			self.plot.fill('blue')
		elif self.state == 1:
			self.plot.fill('black')
		elif self.previous == 1 and self.state == 0:
			self.plot.fill('red')
		else:
			self.plot.fill('white')
		self.plot.rect(self.x*self.w, self.y*self.w, self.w, self.w)

	def update(self):
		neighbors = 0
		for i in range(-1, 2):
			for j in range(-1, 2):
				neighbors += self.board[self.x+i][self.y+j].previous
		neighbors -= self.board[self.x][self.y].previous
		if self.previous == 1 and neighbors < 2:
			self.state = 0
		elif self.previous == 1 and neighbors > 3:
			self.state = 0
		elif self.previous == 0 and neighbors == 3:
			self.state = 1

class Game:

	def __init__(self, plot, w=10):
		self.w = w
		self.plot = plot
		self.rows = int(self.plot.width/self.w)
		self.cols = int(self.plot.height/self.w)
		self.board = []
		for j in range(self.rows):
			self.board.append([])
			for i in range(self.cols):
				newCell = Cell(i, j, w, self.plot, self.board)
				newCell.previous = random.randint(0,1)
				self.board[j].append(newCell)

	def display(self):
		for j in range(1,self.rows-1):
			for i in range(1,self.cols-1):
				self.board[j][i].display()
				self.board[j][i].previous = self.board[j][i].state

	def update(self):
		for j in range(1,self.rows-1):
			for i in range(1, self.cols-1):
				self.board[j][i].update()

class gamePlotter(Plotter):

	def setup(self):
		pass

	def draw(self):
		self.clear()
		self.game.update()
		self.game.display()

if __name__ == '__main__':
	p = gamePlotter()
	g = Game(plot=p)
	p.game = g
	p.mainloop()

