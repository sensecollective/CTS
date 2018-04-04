from Data import *

class Graph(Data):
	
	def __init__(self, directed=True):
		super().__init__()
		self.links = []
		self.labels = []

	def link(self, initial, final):
		pair = [initial, final]
		self.links.append(pair)
		self.labels.append([])

	def label(self, index, label):
		self.labels[index] = label

	def getlinks(self):
		links = []
		for i in range(len(self.links)):
			links.append([])
			for j in range(len(self.links[i])):
				links[i].append(self.get(self.links[i][j]))
		return links


	def getlabels(self):
		labels = []
		for i in range(len(self.labels)):
			labels.append([])
			for j in range(len(self.labels[i])):
				labels[i].append(self.get(self.labels[i][j]))
		return labels

	def compute(self, index):
		link = self.links[index]
		labels = self.labels[index]
		for i in range(len(link)):
			link[i] = self.get(link[i])
		for i in range(len(labels)):
			labels[i] = self.get(labels[i])
		return compute(link, labels)
		
	def neighbors(self, key, directed=True):
		index = key
		neighbors = []
		for i in range(len(self.links)):
			if index in self.links[i]:
				if index == self.links[i][0]:
					neighbors.append(self.links[i][1])
				elif index == self.links[i][1] and not directed:
					neighbors.append(self.links[i][0])
		return neighbors
	
	def generate(self, operators):
		opkeys = operators
		ops = []
		for i in range(len(opkeys)):
			ops.append(self.get(opkeys[i]))
		links = self.getlinks()
		outputs = []
		for i in range(len(links)):
			outputs.append(compute(links[i], ops))
		for i in range(len(outputs)):
			f = []
			for j in range(len(outputs[i])):
				if outputs[i][j] == True:
					f.append(opkeys[j])
			self.label(i, f)
	
	def analyze(self):
		labels = self.getlabels()
		links = self.getlinks()
		outputs = []
		for i in range(len(links)):
			output = select(links[i], labels[i], istrue)
			for j in range(len(output)):
				output[j] = self.labels[i][output[j]]
			outputs.append(output)
		return outputs

	def direct(self):
		self.links = direct(self.links)

	def model(self):
		output = dict()
		labels = self.analyze()
		for i in range(len(self.links)):
			a, b = self.links[i]
			if a not in Keys(output):
				output[a] = dict()
			output[a][b] = labels[i]
		return output