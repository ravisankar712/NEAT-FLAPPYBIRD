import numpy as np
import NeuralNetwork as nn
import pygame as pg

g = 1.5	#gravity
pg.init()

width = 600
height = 600
world = pg.display.set_mode((width, height))

class Bird():

	def __init__(self):

		self.x = width/3.0
		self.y = height/2.0
		self.vel = 0
		self.r = 15
		self.force = 18
		self.dna = nn.NeuralNetwork(5, 2, 1, 4) #dna is a neural network.
		self.dna.Set_Mutationrate(0.1)
		self.fitness = 0
		self.highlight = False

	def update(self):

		self.vel -= g
		self.y -= self.vel
		self.fitness += 1

	def show(self):

		if self.highlight:
			pg.draw.circle(world, (255, 0, 0), [int(self.x), int(self.y)], self.r)
		else:
			pg.draw.circle(world, (207, 80, 68), [int(self.x), int(self.y)], self.r)


	def edges(self):

		if self.y + self.r > height  or self.y - self.r < 0:
			return True

	def choose(self, pipes):

		#input to the neural network are, height, y velocity, length to the closest pipe, top and bottom of closest pipe
		closest_pip = self.Findclosest(pipes)
		inp = [self.y*1.0/height, self.vel*1.0/self.force, closest_pip.x*1.0/width, closest_pip.top*1.0/height, closest_pip.bottom*1.0/height]
		out = np.argmax(self.dna.Guess(inp))
		if out == 1:
			self.jump()
		else:
			pass

		# out = self.dna.Guess(inp)
		# if out[1] > out[0]:
		# 	self.jump(out[2])
		# else:
		# 	pass

	def Findclosest(self, pipes): #finds the pipe closest to the bird, which is not behind

		if pipes[0].x + pipes[0].w - self.x> 0:
			return pipes[0]
		else:
			return pipes[1]

	def jump(self):

		# if self.vel < -30:		#dont jump when bird is already moving up with speed 35
		# 	pass
		# else:
		self.vel += self.force

	def Death(self, pipes):

		death = False
		if self.edges():
			death = True

		for p in pipes:
			if p.collision(self):
				death = True
		return death
