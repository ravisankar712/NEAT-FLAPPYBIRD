import numpy as np
import pygame as pg


width = 600
height = 600
world = pg.display.set_mode((width, height))

pg.init()

class Pipe():

	def __init__(self):

		self.x = width
		self.w = 50
		self.bottom = np.random.random() * height * (0.75) + height/4
		self.gap =  150
		self.top = self.bottom - self.gap
		self.vel = 5


	def show(self):

		pg.draw.rect(world, (0, 200, 100), (int(self.x), int(self.bottom), self.w, height - self.top))
		pg.draw.rect(world, (0, 200, 100), (int(self.x), 0, self.w, self.top))


	def update(self):

		self.x -= self.vel

	def done(self):
		if self.x < -self.w:
			return True

	def collision(self, bird):

		if bird.y + bird.r > self.bottom or bird.y - bird.r < self.top:
			if bird.x + bird.r > self.x and bird.x - bird.r < self.x + self.w  :
				return True

