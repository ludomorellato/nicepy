from functions.create_regions_as_classes import regions_as_classes
from functions.sanity_checks import check_all_edges_twice
from functions.compute_distance import compute_distance
from functions.compute_neighbours import compute_neighbours
from functions.compute_circles_and_arcs import compute_curves_diagram
from functions.compute_distance_complexities_diagram import compute_distance_complexities_diagram
from functions.compute_number_generators import compute_number_generators

from algorithm_functions.finger_move_beginning_bordered import finger_move_beginning_bordered
from algorithm_functions.Sarkar_Wang_algorithm_smart import Sarkar_Wang_algorithm_smart




class Heegaard_diagram:

	def __init__(
		self, 
		number_intersection_points, 
		number_border_points, 
		regions_input, 
		basepoints_dictionary, 
		last_diagram_regions_modified
		):
		
		# We create regions as classes
		self.regions = regions_as_classes(regions_input, number_border_points)


		# We compute now the lists of list that describe the alpha circles, alpha arcs and the blue circles.
		# This is superfluous the first time, but not all the other times
		curves_diagram = compute_curves_diagram(
			regions_input, 
			number_border_points, 
			number_intersection_points
			)

		red_arcs = curves_diagram['red_arcs']
		red_circles = curves_diagram['red_circles']
		blue_circles = curves_diagram['blue_circles']
		

		# We assign the others attributes
		self.number_of_regions = len(self.regions)
		self.is_nice = False
		self.red_circles = red_circles
		self.red_arcs = red_arcs
		self.blue_circles = blue_circles
		self.number_intersection_points = number_intersection_points
		self.number_border_points = number_border_points
		self.regions_input = regions_input

		self.border_regions = []

		for i in self.regions.keys():

			# We compute all the border regions
			if self.regions[i].is_border:
				self.border_regions.append(i)
			else:
				pass
		
		
		# We take note of the data in basepoints_dictionary, setting also a flag which helps
		# us to know if we are working with a  4-ended tangle diagram or not

		self.basepoints_dictionary = basepoints_dictionary

		self.is_tangle_diagram = bool(basepoints_dictionary['p_or_q'])
		self.multiplicity_zero_regions = basepoints_dictionary['multiplicity_zero_regions']
		self.basepoints_p_or_q = basepoints_dictionary['p_or_q']
		self.basepoint_regions_and_red_edges = basepoints_dictionary['basepoint_regions_and_red_edges']


		
		# We eliminate the keys in self.basepoint_regions_and_red_edges that were left without values
		if self.is_tangle_diagram:
			keys_to_delete = []
			for key in self.basepoint_regions_and_red_edges.keys():
				if self.basepoint_regions_and_red_edges[key] == []:
					keys_to_delete.append(key)
		
			for key in keys_to_delete:
				del self.basepoint_regions_and_red_edges[key]


		# Attributes to eventually update the diagram
		self.NEW_regions_input = []
		self.NEW_number_intersection_points = 0
		self.NEW_number_border_points = self.number_border_points

		# Attribute to update when the algorithm runs
		self.last_diagram_regions_modified = last_diagram_regions_modified



		# We run a first sanity check on the constructed diagram, i.e. we check that all 
		# the edges are counted exactly two times in the two different directions 
		check_all_edges_twice(self)


		# We compute the neighbours of the regions and we save them in the .neighbours 
		# attribute of the regions
		compute_neighbours(self)


		# We compute the distances of the regions we save it in the .distance attribute
		# of the regions
		compute_distance(self)


		# Lastly, we compute the distance complexities that we need to run the algorithm
		self.distance_complexities = dict()

		for i in self.regions.keys():

			# We save all the bad regions in the distances dictionary under the right key
			if self.regions[i].distance not in self.distance_complexities.keys():
				if (self.regions[i].distance > 0) and (self.regions[i].badness > 0):
					self.distance_complexities[self.regions[i].distance] = [self.regions[i]]
				else:
					pass
			else:
				if (self.regions[i].distance > 0) and (self.regions[i].badness > 0):
					self.distance_complexities[self.regions[i].distance].append(self.regions[i])
				else:
					pass

		if self.distance_complexities:
			self.distance_diagram = max(self.distance_complexities.keys())
		else:
			self.distance_diagram = 0

		# Needed in the choice of the best next diagram
		(self.distance_complexities, self.total_complexity) = compute_distance_complexities_diagram(self)

		# We compute the number of generators
		self.number_of_generators = compute_number_generators(self)



	# Method to update the diagram
	def update_diagram(self):

		self.basepoints_dictionary['multiplicity_zero_regions'] = self.multiplicity_zero_regions
		self.basepoints_dictionary['p_or_q'] = self.basepoints_p_or_q
		self.basepoints_dictionary['basepoint_regions_and_red_edges'] = self.basepoint_regions_and_red_edges

		self.__init__(
			self.NEW_number_intersection_points, 
			self.NEW_number_border_points, 
			self.NEW_regions_input, 
			self.basepoints_dictionary, 
			self.last_diagram_regions_modified
		)
		



	# Method for the beginning finger move
	def finger_move_beginning_bordered(self, user_experience):
		intermediate_steps_beginning = finger_move_beginning_bordered(self, user_experience)

		if intermediate_steps_beginning:
			
			number_initial_finger_moves = intermediate_steps_beginning['number_finger_moves']

			# We actually generate Heegaard Diagrams
			intermediate_steps_beginning_diagrams = dict()
			for step_number in range(number_initial_finger_moves + 1):
				intermediate_steps_beginning_diagrams[step_number] = Heegaard_diagram(
					intermediate_steps_beginning[step_number][0], 
					intermediate_steps_beginning[step_number][1], 
					intermediate_steps_beginning[step_number][2], 
					intermediate_steps_beginning[step_number][3], 
					intermediate_steps_beginning[step_number][4]
					)

			# We print the changes done on the initial diagram
			print('\n')
			print('The initial finger moves worked!\n')
			print('\n')
			print(f'Number of finger moves done: {number_initial_finger_moves} \n')
			print('\n')
			print('These are the intermediate step, including the starting diagram and the finishing one:\n')

			if user_experience:
				input('\nPress enter to continue...')
				print('\n')

			for step_number in intermediate_steps_beginning_diagrams.keys():
				print('-----------------------------------------------------------------------')
				print('\n')
				print('\n')
				print(f'Step number {step_number}: \n')
				print(intermediate_steps_beginning_diagrams[step_number])
				print('\n')
				print('\n')

			print("From now on, we'll take this last diagram as 'step 0' diagram \n")

			if user_experience:
				input('\nPress enter to continue...')
			
			print('\n \n')




	# Method for apply the algorithm to the diagram
	def Sarkar_Wang_algorithm(self):
		Sarkar_Wang_algorithm_smart(self)



	# Method called when we write simply "diagram"
	def __repr__(self):
		return "This is a Heegaard diagram"

	# Method called when we write "print(diagram)"
	def __str__(self):
		s = "Details of the Heegaard diagram:"

		s = s + "\n"
		s = s + f"\n	Is it nice: {self.is_nice}"

		if not self.is_nice:
			s = s + "\n"
			s = s + f"\n		Distance of the diagram: {self.distance_diagram}"
			s = s + "\n		Distance complexities of the diagram: "
			for distance in self.distance_complexities:
				s = s + f"\n			Total badness of distance {distance}: {self.distance_complexities[distance][0]}"
				s = s + f"\n			Ordered list of badnesses and respectively regions: {self.distance_complexities[distance][1:]}"

		s = s + "\n"
		s = s + f"\n	Number of regions: {self.number_of_regions}"
		s = s + f"\n	Number of intersection points: {self.number_intersection_points}"
		s = s + f"\n	Number of border points: {self.number_border_points}"
		s = s + "\n"

		if self.last_diagram_regions_modified:
			s = s + "\n	Regions of the last diagram that we modified: "

			s = s + f"\n		Type of move: {self.last_diagram_regions_modified[-1]}"
			s = s + f"\n		Starting region: Region {self.last_diagram_regions_modified[0]}"
			s = s + f"\n		Edge modified: {self.last_diagram_regions_modified[1]}"
			s = s + f"\n		Ending region: Region {self.last_diagram_regions_modified[-3]}"
			s = s + f"\n		neighbour region: Region {self.last_diagram_regions_modified[-2]}"
			s = s + f"\n		Middle regions:"

			if self.last_diagram_regions_modified[2] == []:
				s = s + " None"
			else:
				for label in self.last_diagram_regions_modified[2]:
					s = s + f"\n			Region {label}"
			
			s = s + "\n		Edges crossed:"
			for edge in self.last_diagram_regions_modified[3]:
				s = s + f"\n			{edge}"

			s = s + "\n"
		
		s = s + "\n	Regions of the diagram: "
		for label in self.regions:
			temp = f"\n		Region {self.regions[label].label}:"
			temp = temp+ f"\n			Input: {self.regions[label].input}"
			temp = temp+ f"\n			Badness: {self.regions[label].badness}"
			if self.regions[label].distance != -1:
				temp = temp + f"\n			Distance: {self.regions[label].distance}"
			temp = temp+ f"\n			Is a border region: {self.regions[label].is_border} \n"

			s = s + temp
		
		s = s + "\n"
		
		
		return s
