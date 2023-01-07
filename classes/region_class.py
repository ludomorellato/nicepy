class Region:
	def __init__(self, label, n, red_edges, blue_edges, border_edges, input):
		self.label = label
		self.number_edges = 2*n
		self.badness = max(n-2,0)
		self.red_edges = red_edges #[[1,2], ... [1,3]]
		self.blue_edges = blue_edges #[[1,2], ... [1,3]]
		self.border_edges = border_edges #[[1,2], ... [1,3]]
		self.distance = -1
		self.red_neighbors = []
		self.blue_neighbors = []
		self.input = input
		
		if border_edges:
			self.is_border = True
		else:
			self.is_border = False

		# In the case of a 4-ended tangle diagram, we want to know if a region with a basepoint
		# is inside of the alpha arcs of outside. To keep track of this, we set this attribute
		# that we modify when we assign the distance of a region (remark that every region is
		# going to have this attribute, even if it doesn't contain a basepoint)
		self.p_or_q = False


	def add_neighbor(self, neighbor, color):
			if color == 'red':
				self.red_neighbors.append(neighbor)
			elif color == 'blue':
				self.blue_neighbors.append(neighbor)
        
        
	# Method called when we write simply "regions[i]"
	def __repr__(self):
		return "Region %d" %self.label

	# Method called when we write "print(regions[i])"
	def __str__(self):
		s = "Region "+ str(self.label) + ":"
		s = s+ "\n	Badness: " + str(self.badness)
		if self.distance != -1:
			s = s + "\n	Distance: " + str(self.distance)
		s = s+ "\n	Input: " + str(self.input)
		s = s+ "\n		Red edges: " + str(self.red_edges)
		s = s+ "\n		Blue edges: " + str(self.blue_edges) + "\n"
		s = s+ "\n	Red neighbors: "+ str(self.red_neighbors) 
		s = s+"\n	Blue neighbors: " + str(self.blue_neighbors)
		s = s+"\n	Is a border region: " + str(self.is_border) + "\n \n"

		return s

