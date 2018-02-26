from Frame import *
from Functions import *
from Operations import *

class System:
	def __init__(self, variables, functions, operations):
		var = dict()
		for v in variables:
			var[v] = None 
		variables = var

		fun = dict()
		for i in range(len(functions)):
			f = functions[i]
			o = operations[i]
			fun[f] = o 
		functions = fun

		self.variables = variables
		self.functions = functions

	def getvariable(self, name):
		return self.variables[name]

	def getfunction(self, name):
		return self.functions[name]

def Object(T, N, I, C):
	frame = Frame(T)
	frame['class'] = N
	frame['index'] = I
	frame['children'] = C
	return frame

class Interpreter:

	def __init__(self, F, V):
		self.system = F
		self.variables = V
	def compute(self, object, input):
		P = input['parents']
		I = object['index']
		if I in P:
			Y = [I]
			C = object['children']
			for child in C:
				V = self.compute(child, input)
				if V != []: return Y + V
			return [I]
		return []

	def append(self, tree, object, directory):
		O = tree
		history = list()
		indices = list()
		for i in range(1, len(directory)):
			children = O['children']	
			for j in range(len(children)):
				if children[j]['index'] == directory[i]:
					history.append(O)
					indices.append(j)
					O = children[j]
					break

		O['children'].append(object)
		for i in range(len(history)-1, -1, -1):
			history[i]['children'][indices[i]] = O
			O = history[i]
			del history[i]
		return O

	def construct(self, model):
		functions = []
		structures = []
		variables = []
		for i in range(len(model)):
			O = model[i]
			if O['type'] == 'structure':
				structures.append(O)
			elif O['type'] == 'function':
				functions.append(O)
			else:
				variables.append(O)
		elements = variables + functions + structures

		tree = None
		for i in range(len(elements)-1, -1, -1):
			P = elements[i]['parents']
			if tree == None and len(P) == 0:
				C = elements[i]['type']
				N = elements[i]['class']
				tree = Object(C, N, i, list())
			else:
				directory = self.compute(tree, elements[i])
				C = elements[i]['type']
				N = elements[i]['class']
				X = Object(C, N, i, list())
				tree = self.append(tree, X, directory)
		
		return tree
		# elements = functions + variables
		# for i in range(len(elements)):
		# 	P = elements[i]['parents']
		# 	directory = self.compute(tree, elements[i])
		# 	tree = self.append(tree, elements[i], directory)

		# for i in range(len(variables)):
		# 	P = variables[i]['parents']
		# 	directory = self.compute(tree, variables[i])
		# 	tree = self.append(tree, variables[i], directory)
	def convert(self, object):
		T = object['type']
		if T == 'structure':
			C = object['children']
			for i in range(len(C)):
				C[i] = self.convert(C[i])
				print(C[i])
			F = None
			for i in range(len(C)):
				if C[i]['type'] == 'function':
					F = C[i]
					del C[i]
					break
			print(C)
			object = Operation(F, C)

		elif T == 'function':
			C = object['class']
			F = self.system[C]
			object = Function(F)

		elif T == 'variable':
			C = object['class']
			V = self.variables[C]
			object = Value(V)
		return object

	def __call__(self, sentence):
		sentence = revise(sentence)
		boundaries = mark(sentence, self.system)

		indices = []
		for i in range(len(boundaries)):
			indices.append(boundaries[i][1])
	
		string = ''
		names = []
		elements = []
		for i in range(len(sentence)):
			if i not in indices:
				string += sentence[i]
			elif string != '':
				elements.append(['variable', i-len(string)])
				elements.append(['/variable', i-1])
				names.append(string)
				string = ''
		elements = define(elements)
		for i in range(len(elements)):
			elements[i] = [names[i], elements[i][1], 'variable']
		
		model = create(elements + define(boundaries))
		print(model)
		tree = self.construct(model)
		output = self.convert(tree)
		return output
		# rules = {'and':AND, 'or':OR}
		# output = convert(sentence, tree, rules)
		# return output
