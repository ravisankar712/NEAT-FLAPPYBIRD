import pygame as pg
import Bird as bird
import Pipe as pipe
import numpy as np

pg.init()
pg.font.init()
pg.display.init()
myfont = pg.font.SysFont('times', 25)

width = 640
height = 480
#swtting the same dimensions for the bird and pipe classes
pipe.width = width
bird.width = width
pipe.height = height
bird.height = height
counter = 0
cycles = 1
pipe_freq = 70 #new pipe is added after these many frames
world = pg.display.set_mode((width, height))
clock = pg.time.Clock()

gen = 1
pop_size = 100
Population = [bird.Bird() for i in range(pop_size)] #creates the initial bird population
gene_pool = []
pipes = []

#creating the next generation based on fitness
def NextGen(pool):

	#normalise fitness
	total = 0.0
	for b in pool:
		total += b.fitness
	for b in pool:
		b.fitness /= total

	next_gen = []

	'''take the best bird to next gen for free!! if using this, then change the range of next loop to pop_size-1'''
	# index = Find_Best(pool)
	# dna = pool[index].dna.Clone()
	# child = bird.Bird() #new bird object
	# #child's dna is set equal to the parent dna
	# child.dna.Set_Weights(dna.weights)
	# child.dna.Set_Biases(dna.biases)
	# # child.highlight = True
	# next_gen.append(child)
	for _ in range(pop_size):
		newBird = makeChild(pool)
		next_gen.append(newBird)

	return next_gen

def makeChild(pool):

	#the procedure to select a new parent. The more the fitness, the more chance that it gets selected
	N = 0
	r = np.random.random()
	while r > 0:
		r -= pool[N].fitness
		N += 1
	N -= 1
	#the parent clones its dna
	dna = pool[N].dna.Clone()
	dna.Mutate() #mutation. TO CHANGE MUTATION RATE, GOTO THE bird.py FILE
	child = bird.Bird() #new bird object
	#child's dna is set equal to the parent dna
	child.dna.Set_Weights(dna.weights)
	child.dna.Set_Biases(dna.biases)

	return child

def Find_Best(pool):
	index = 0
	for i in range(1, len(pool), 1):
		if pool[i].fitness > pool[index].fitness:
			index = i
	return index

def show_text():
	textsurface = myfont.render('Generation = ' + str(gen), False, (231, 210, 0))
	world.blit(textsurface, (0, 0))
	# textsurface1 = myfont.render('Speed:: ' + str(cycles), False, (255, 255, 255))
	# world.blit(textsurface1, (width - 110, 0))
	textsurface2 = myfont.render('Birds alive  = ' + str(len(Population)), False, (231, 210, 0))
	world.blit(textsurface2, (0, 25))
	textsurface3 = myfont.render('Best Fitness = ' + str(max_fit), False, (249, 160, 71))
	world.blit(textsurface3, (int(width/2) - 50, 0))
	textsurface4 = myfont.render('Curr Fitness = ' + str(curr_fit), False, (249, 160, 71))
	world.blit(textsurface4, (int(width/2) - 50, 25))

#gameloop
max_fit = 0
curr_fit = 0
show_best = False
recording = False
file_num = 0

while True:

	for event in pg.event.get():
		if event.type == pg.QUIT:
			pg.quit()
			quit()
		#cycle controls game speed
		if event.type == pg.KEYDOWN:
			if event.key == pg.K_UP:
				cycles += 1
			if event.key == pg.K_DOWN:
				if cycles > 1:
					cycles -= 1
				else:
					pass
			if event.key == pg.K_b:
				show_best = not show_best
			if event.key == pg.K_r:
				recording = not recording
			if event.key == pg.K_q:
				pg.quit()
				quit()


	world.fill((26, 44, 77))
	#show pipes
	for p in pipes:
		p.show()

	#show birds
	if len(Population) > 0:
		index = Find_Best(Population)
		curr_fit = Population[index].fitness
		max_fit = max(curr_fit, max_fit)
		if show_best:#only show the best bird
			Population[index].highlight = True
			Population[index].show()

		else:#show all birds
			for b in Population:
				b.show()

	show_text()#show the numbers

	for frame in range(cycles): #number of calcs done per frame

		if counter % pipe_freq == 0:
			pipes.append(pipe.Pipe())
		counter += 1

		for p in pipes:
			p.update()
		if pipes[0].done():
			pipes.remove(pipes[0])

		if len(Population) != 0:
			for b in Population:
				b.choose(pipes)
				b.update()
				if b.Death(pipes):
					Population.remove(b)
					gene_pool.append(b)
		else:
			pipes.clear()
			counter = 0
			Population = NextGen(gene_pool)
			gene_pool = []
			gen += 1

	if recording:
		file_name = "snaps\\gen1to40\\{}.png".format(str(file_num))
		pg.image.save(world, file_name)
		file_num += 1
	pg.display.update()
	clock.tick(60)
