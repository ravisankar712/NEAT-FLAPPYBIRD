import numpy as np 
import copy

#activation function
#derivative of sigma is actially sig(x) * (1 - sig(x)). 
# But we call this function with an array which aleardy is applied with sig 
def sigmoid(x, derivative=False):
	if derivative:
		return x * (1 - x)
	else:
		return 1.0/(1.0 + np.exp(-x))

def tanh(x, derivative=False):
	if derivative:
		return  1.0 - x**2
	else:
		return np.tanh(x)

def SoftMax(x):
	num = np.exp(x)
	return num/np.sum(num)

class NeuralNetwork():

	#takes in number of input nodes, output nodes, number of hidden layers, number of nodes in each hidden layer
	def __init__(self, Nin, Nout, NHL, NHN):
		self.Nin = Nin
		self.Nout = Nout
		self.NHL = NHL
		self.NHN = NHN
		self.learning_rate = 0.01
		self.activation_fn = 'tanh'
		self.mutation_rate = 0.01
	
		#initialise weights and biases randomly
		if self.NHL == 0:
			self.weights = [np.random.random((Nout, Nin))]
			self.biases = [np.zeros(Nout)]
		else:
			self.weights = [np.random.random((NHN, Nin))]
			self.biases = [np.zeros(NHN)]
			for i in range(NHL - 1):
				self.weights.append(np.random.random((NHN, NHN)))
				self.biases.append(np.zeros(NHN))
			self.weights.append(np.random.random((Nout, NHN)))
			self.biases.append(np.zeros(Nout))

	def Activation(self, inp, derivative = False):
		if self.activation_fn == 'sigmoid':
			return sigmoid(inp, derivative)
		elif self.activation_fn == 'tanh':
			return tanh(inp, derivative)

	#feedforward algorithm. inp must be an array of length Nin
	def FeedForward(self, inp):
		output = np.array(inp)
		all_layers = [output]
		for i in range(self.NHL + 1):
			output = self.Activation(np.dot(self.weights[i], output) + self.biases[i])
			all_layers.append(output)
		return all_layers

	def Guess(self, inp):
		output = self.FeedForward(inp)[-1]
		return output

	def BackPropagate(self, inp, target):
		all_layers = self.FeedForward(inp)

		err = np.array(target) - all_layers[-1]
		#backpropagation algorithm
		for i in range(self.NHL + 1):
			#grad_j(L) = err_J(L) * sig'(layer_j(L))
			grad = err * self.Activation(all_layers[self.NHL - i + 1], True) 
			#dW_jk(b/w L and L+1) = grad_j(L) x layer_k(L-1)
			delta_W = self.learning_rate * np.outer(grad, all_layers[self.NHL - i]) 
			delta_b = self.learning_rate * grad
			self.weights[self.NHL - i] += delta_W
			self.biases[self.NHL - i] += delta_b
			#err(L-1) = W(L-1 to L).transpose x err(L)
			err = np.dot(self.weights[self.NHL - i].transpose(), err) 

	def Train(self, indata, targets, epochs = 10):
		n = len(indata)
		for e in range(epochs):
			for i in range(n):
				N = np.random.randint(n)
				self.BackPropagate(indata[N], targets[N])

	def Calc_Loss(self, inp, target):
		out = self.Guess(inp)
		loss = 0.5 * np.sum((target - out)**2)
		return loss

	def Set_Learningrate(self, lr):
		self.learning_rate = lr

	def Set_Weights(self, weights):
		self.weights = weights

	def Set_Biases(self, biases):
		self.biases = biases

	def Set_Activation(self, choice):
		self.activation_fn = choice

	def Set_Mutationrate(self, mr):
		self.mutation_rate = mr

	##methods for genetic algorithm
	def Clone(self):
		new = copy.deepcopy(self)
		return new

	def Crossover(self, other):
		parent1 = copy.deepcopy(self)
		parent2 = copy.deepcopy(other)

		child = NeuralNetwork(parent1.Nin, parent1.Nout, parent1.NHL, parent1.NHN)
		cross_point_W = np.random.randint(len(parent1.weights))
		child.weights = parent1.weights[:cross_point_W] + parent2.weights[cross_point_W:]
		cross_point_b = np.random.randint(len(parent1.biases))
		child.biases = parent1.biases[ : cross_point_b] + parent2.biases[cross_point_b :]

		return child

	def Mutate(self):
		# for i in range(len(self.weights)):
		# 	if np.random.random() < self.mutation_rate:
		# 		self.weights[i] += np.random.normal(0 , 0.1, self.weights[i].shape)
		# for i in range(len(self.biases)):
		# 	if np.random.random() < self.mutation_rate:
		# 		self.biases[i] += np.random.normal(0 , 0.1, self.biases[i].shape)

		for i in range(len(self.weights)):
			row, col = self.weights[i].shape
			for x in range(row):
				for y in range(col):
					if np.random.random() < self.mutation_rate:
						self.weights[i][x, y] += np.random.normal(0 , 0.1)
		for i in range(len(self.biases)):
			row = self.biases[i].shape[0]
			for x in range(row):
				if np.random.random() < self.mutation_rate:
					self.biases[i][x] += np.random.normal(0 , 0.1)