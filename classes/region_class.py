class Region:
	def __init__(self, label, n, red_edges, blue_edges, border_edges, input):
		self.label = label
		self.number_edges = 2*n
		self.badness = max(n-2,0)
		self.red_edges = red_edges #[[1,2], ... [1,3]]
		self.blue_edges = blue_edges #[[1,2], ... [1,3]]
		self.border_edges = border_edges #[[1,2], ... [1,3]]
		self.distance = -1
		self.red_neighbours = []
		self.blue_neighbours = []
		self.input = input
		
		if border_edges:
			self.is_border = True

			# We check if it a border region of a component with alpha or beta arcs
			if len(self.red_edges) > len(self.blue_edges):
				self.border_alpha_arcs = True
				self.border_beta_arcs = False
			else:
				self.border_alpha_arcs = True
				self.border_beta_arcs = False

		else:
			self.is_border = False
			self.border_alpha_arcs = False
			self.border_beta_arcs = False

		# In the case of a 4-ended tangle diagram, we want to know if a region with a basepoint
		# is inside of the alpha arcs of outside. To keep track of this, we set this attribute
		# that we modify when we assign the distance of a region (remark that every region is
		# going to have this attribute, even if it doesn't contain a basepoint)
		self.p_or_q = False


	def add_neighbour(self, neighbour, color):
			if color == 'red':
				self.red_neighbours.append(neighbour)
			elif color == 'blue':
				self.blue_neighbours.append(neighbour)
        
        
	# Method called when we write simply "region"
	def __repr__(self):
		return f"Region {self.label}"

	# Method called when we write "print(region)"
	def __str__(self):
		s = f"Region {self.label}" + ":"
		s = s+ f"\n	Badness: {self.badness}"
		if self.distance != -1:
			s = s + f"\n	Distance: {self.distance}"
		s = s+ f"\n	Input: {self.input}"
		s = s+ f"\n		Red edges: {self.red_edges}"
		s = s+ f"\n		Blue edges: {self.blue_edges}\n"
		s = s+ f"\n	Red neighbours: {self.red_neighbours}" 
		s = s+ f"\n	Blue neighbours: {self.blue_neighbours}"
		s = s+ f"\n	Is a border region: {self.is_border}"
		if self.is_border:
			if self.border_alpha_arcs:
				s = s + f"	It's a border region with alpha arcs"
			else:
				s = s + f"	It's a border region with beta arcs"
		s = s + "\n \n"

		return s

