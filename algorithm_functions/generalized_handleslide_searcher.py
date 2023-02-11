import copy

from functions.get_index_of_edge import get_index_of_edge


def generalized_handleslide_searcher(diagram, starting_region_label, edge_to_modify, edge_to_modify_index):

	starting_region = diagram.regions[starting_region_label].input

	possible_couple_edges = neighbour_edge_searcher(diagram, starting_region, edge_to_modify, edge_to_modify_index)
	
	possible_generalized_handleslides = dict()

	for possibility in possible_couple_edges.keys():
		
		red_edge_to_go_through = possible_couple_edges[possibility]['red_edge_to_go_through']
		circle_set = possible_couple_edges[possibility]['circle']

		# We create the new entry in the possible_generalized_handleslides dictionary
		possible_generalized_handleslides[tuple(red_edge_to_go_through)] = dict()

		possible_move_temp = generalized_handleslide_construction(diagram, starting_region_label, edge_to_modify, red_edge_to_go_through, circle_set)

		possible_generalized_handleslides[tuple(red_edge_to_go_through)]['starting_region_label'] = starting_region_label
		possible_generalized_handleslides[tuple(red_edge_to_go_through)]['regions_to_go_through'] = possible_move_temp['regions_to_go_through']
		possible_generalized_handleslides[tuple(red_edge_to_go_through)]['edges_to_go_through'] = possible_move_temp['edges_to_go_through']
		possible_generalized_handleslides[tuple(red_edge_to_go_through)]['edge_to_slide'] = possible_move_temp['edge_to_slide']
		possible_generalized_handleslides[tuple(red_edge_to_go_through)]['circle'] = possible_move_temp['circle']
		

	return possible_generalized_handleslides







def neighbour_edge_searcher(diagram, starting_region, edge_to_modify, edge_to_modify_index):

	# As first check, if we only have one blue circle we don't
	# have any chance; therefore we return False
	if len(diagram.blue_circles) == 1:
		return dict()
	

	# Otherwise, we can try to find these generalized handleslide

	# We construct a list of all the circles in the form of sets
	blue_circles_set = []
  
	for circle in diagram.blue_circles:

		# We copy the blue circles and we append them as set in blue_circles_set
		blue_circles_set.append(set(circle.copy()))


	
	# We want to understand if there are two blue edges in starting_region that 
	# are next to each other and such that they are of the same blue circle


	# To do so, we eliminate the blue circle on which edge_to_modify
	# stays from the list of circles that we try

	set_edge_to_modify = set(edge_to_modify)

	for circle in blue_circles_set:

		if set_edge_to_modify < circle:

			break

	# We remove the circle that edge_to_modify is on from the list
	blue_circles_set.remove(circle)


	# We now search for edges on the same blue circle
	# To do so, we take the starting region input as a set and we 
	# compute the intersections with the remaining edges

	# We create the set of the starting region and we count the number of edges
	set_starting_region = set(starting_region)
	number_edges_starting_regions = len(starting_region)

	# We create a list with the possible couple of edges
	possible_couple_edges = dict()

	for circle in blue_circles_set:

		# We intersect circle and starting region
		intersection_temp = circle.intersection(set_starting_region)

		# We prepare the list for the eventual points found
		indicies_points = []


		'''
		THIS IS IF WE WANT TO HAVE AT LEAST TWO EDGES ON CIRCLE
		But I think that it is not helpful

		# We check how many intersection points we have
		if len(intersection_temp) > 3:

			# We have at least two edges in the region that stay on circle
			# We need to understand where they are. We create a list
			# of the form (index, point)

			for point in intersection_temp:
				indicies_points.append((starting_region.index(point), point))
		'''

		for point in intersection_temp:
			indicies_points.append((starting_region.index(point), point))

		# We now check if there are some verticies at the right distance

		# To do so, we create a dictionary with the edges that we have found,
		# using the lower index as key
		edges_found = dict()

		while indicies_points:
		
			# We take the first couple
			(index, point) = indicies_points[0]

			# We look for the other point that form an edge in the region
			for (other_index, other_point) in indicies_points[1:]:
		
				if ((index - other_index == 1) or (index - other_index == -number_edges_starting_regions + 1)) and (other_index % 2 == 1):
					
					# We have found the other point that form the edge with point
					# and we have that index > other_index

					edges_found[other_index] = [other_point, point]
					break
					
				elif ((index - other_index == -1) or (index - other_index == number_edges_starting_regions - 1)) and (index % 2 == 1):

					# We have found the other point that form the edge with point
					# and we have that other_index > index

					edges_found[index] = [point, other_point]
					break

			# We remove both points from the iterable list
			indicies_points.remove((index, point))
			indicies_points.remove((other_index, other_point))



		# We have now a dictionary with all the blue edges in starting_region 
		# that stay on circle





		# We first see if we have indeed some edge
		if not edges_found:

			# In this case, we pass to the next cycle of the while cycle, as it means that
			# we don't have the possibility for a handleslide with this circle
			pass




		else:

			# We have found some edge, hence we can try to see if we have a possible handleslide to execute


			# We want to split starting_region in the best possible way:
			# The best possible way, would be to leave one square instead of starting_region.
			# If this is not possible, we try to find the longest sequence of successive blue edges 
			# that are on circle and we take the two most distant ones (but remembering to leave 
			# squares on the sides; otherwise we choose one point randomly (CAN THIS BE OPTIMIZED?)
			
			# Notice that with the generalized handleslide we can make the badness decrease by 2, 
			# therefore it is actually conveniente to split the region in regions with even badnesses
			

			# We want to check if there are blue edges that are different from edge_to_modify_index + 2 and 
			# edge_to_modify_index - 2
			
			# We set a backup edge in the cases in which we only have one (or two) of the above edges
			
			# We check the blue edge on the right
			if ((edge_to_modify_index + 2) % number_edges_starting_regions) in edges_found.keys():
				
				# We take as backup edge the red edge immediately after
				first_index = (edge_to_modify_index + 3) % number_edges_starting_regions
				backup_red_edge = starting_region[first_index: first_index + 2]

				# We remove this edge from edges_found
				del edges_found[(edge_to_modify_index + 2) % number_edges_starting_regions]


			# We check the blue edge on the left
			if ((edge_to_modify_index - 2) % number_edges_starting_regions) in edges_found.keys():
				
				# We take as backup edge the red edge immediately after
				first_index = (edge_to_modify_index -1) % number_edges_starting_regions
				backup_red_edge = starting_region[first_index: first_index + 2]

				# We remove this edge from edges_found
				del edges_found[(edge_to_modify_index - 2) % number_edges_starting_regions]

			
			# We check if we still have some indicies to search through
			if not edges_found:

				# In this case, we use backup_red_edge as red edge
				red_edge_to_go_through = backup_red_edge

			else:

				# We have some other edge that we can use

				# We understand the badness of the region
				if number_edges_starting_regions % 4 == 0:
					even_badness = True
				else:
					even_badness = False



				# We now find a suitable edge. The only case to pay attention to is the one in which
				# the badness is even and therefore we wold prefer to split it evenly
				if even_badness:
					
					# We set red_edge_to_go_through to False, to check afterwards if we found it or not
					red_edge_to_go_through = False

					# We want to look for some indicies of the form edge_to_modify_index + 4*k
					for index_blue_edge in edges_found.keys():

						if ((index_blue_edge - edge_to_modify_index) % 4 == 0):

							# We can use this red edge
							first_index = (index_blue_edge + 1) % number_edges_starting_regions
							red_edge_to_go_through = starting_region[first_index: first_index + 2]

							# And we break the cycle
							break
					
					# We check if we didn't find the red edge
					if not red_edge_to_go_through:

						# In this case, we take another red edge (they are equivalent)
						first_index = (list(edges_found.keys())[0] + 1) % number_edges_starting_regions
						red_edge_to_go_through = starting_region[first_index: first_index + 2]

				else:

					# If the badness is odd, we don't have a move that it is clearly better than the others
					# Therefore we take one randomly
					first_index = (list(edges_found.keys())[0] + 1) % number_edges_starting_regions
					red_edge_to_go_through = starting_region[first_index: first_index + 2]

			
		
			# We save that data in the dictionary
			possible_couple_edges[tuple(red_edge_to_go_through)] = dict()
			possible_couple_edges[tuple(red_edge_to_go_through)]['red_edge_to_go_through'] = copy.deepcopy(red_edge_to_go_through)
			possible_couple_edges[tuple(red_edge_to_go_through)]['circle'] = copy.deepcopy(circle)
			

		
	return possible_couple_edges




	'''
	OLD VERSION, A BIT STRANGE (AND PROBABLY NOT NECESSARY)

	while edges_found.keys():

			# We take the first index to check
			index = list(edges_found.keys())[0]

			# We check on all the other indicies
			for other_index in edges_found.keys():

				# If the distance is 2, they are neighbour in starting_region
				if (abs(index - other_index) == 2) or (abs(index - other_index) == number_edges_starting_regions - 2):

					# They are neighbour: we save them in the dictionary using the red edge 
					# in the middle as key and saving also the circle that they are on

					# We need to understand whether index > other_index or the other way around
					# and if they are one at the end and one at the beginning of the region's input
					if other_index == 1 and index == number_edges_starting_regions - 1:
						
						# We save the red edge
						red_edge_to_go_through = starting_region[0:2]

						# We generate the dictionary under the key red_edge_to_go_through
						possible_couple_edges[tuple(red_edge_to_go_through)] = dict()

						# We save all the rest of the data
						possible_couple_edges[tuple(red_edge_to_go_through)]['red_edge_to_go_through'] = red_edge_to_go_through
						possible_couple_edges[tuple(red_edge_to_go_through)]['circle'] = circle

					elif index == 1 and other_index == number_edges_starting_regions - 1:
						
						# We save the red edge
						red_edge_to_go_through = starting_region[0:2]

						# We generate the dictionary under the key red_edge_to_go_through
						possible_couple_edges[tuple(red_edge_to_go_through)] = dict()

						# We save all the rest of the data
						possible_couple_edges[tuple(red_edge_to_go_through)]['red_edge_to_go_through'] = red_edge_to_go_through
						possible_couple_edges[tuple(red_edge_to_go_through)]['circle'] = circle

					elif index > other_index:

						# We save the red edge
						red_edge_to_go_through = starting_region[other_index + 1: other_index + 3]

						# We generate the dictionary under the key red_edge_to_go_through
						possible_couple_edges[tuple(red_edge_to_go_through)] = dict()

						# We save all the rest of the data
						possible_couple_edges[tuple(red_edge_to_go_through)]['red_edge_to_go_through'] = copy.deepcopy(red_edge_to_go_through)
						possible_couple_edges[tuple(red_edge_to_go_through)]['circle'] = copy.deepcopy(circle)

					else:

						# We save the red edge
						red_edge_to_go_through = starting_region[index + 1: index + 3]

						# We generate the dictionary under the key red_edge_to_go_through
						possible_couple_edges[tuple(red_edge_to_go_through)] = dict()

						# We save all the rest of the data
						possible_couple_edges[tuple(red_edge_to_go_through)]['red_edge_to_go_through'] = copy.deepcopy(red_edge_to_go_through)
						possible_couple_edges[tuple(red_edge_to_go_through)]['circle'] = copy.deepcopy(circle)


			# We have checked all the possibilities for edges_found[index], we can 
			# remove it from the dictionary
			del edges_found[index] 

		
	return possible_couple_edges





	ANOTHER THING THAT IS NOT HELPFUL

	# The indicies that we would like to find are edge_to_modify_index + 4 
		# or edge_to_modify_index - 4 (recall that we have blue edges in edges_found)

		if ((edge_to_modify_index + 4) % number_edges_starting_regions) in edges_found.keys():
			
			# In this case, we pass through the red edge immediately after
			red_edge_to_go_through = starting_region[(edge_to_modify_index + 5) % number_edges_starting_regions, (edge_to_modify_index + 7) % number_edges_starting_regions]
		
		elif ((edge_to_modify_index - 4) % number_edges_starting_regions) in edges_found.keys():
			
			# In this case, we pass through the red edge immediately after
			red_edge_to_go_through = starting_region[(edge_to_modify_index - 3) % number_edges_starting_regions, (edge_to_modify_index - 1) % number_edges_starting_regions]
		
		else:
			
			# We want to check if there are blue edges that are different from edge_to_modify_index + 2 and 
			# edge_to_modify_index - 2
			
			# We set a backup edge in the cases in which we only have one (or two) of the above edges
			
			# We check the 
			if ((edge_to_modify_index + 2) % number_edges_starting_regions) in edges_found.keys():
				
				# We take as backup edge the red edge immediately after
				backup_red_edge = starting_region[(edge_to_modify_index + 3) % number_edges_starting_regions, (edge_to_modify_index + 5) % number_edges_starting_regions]

			if: 
	'''















def generalized_handleslide_construction(diagram, starting_region_label, edge_to_modify, red_edge_to_go_through, circle_set):
	
	starting_region = diagram.regions[starting_region_label]

	edges_to_go_through = [red_edge_to_go_through]
	regions_to_go_through = []

	# We move the cycle iterating on "middle_region"
	middle_region = starting_region

	# We save the complete circle for later
	circle_list = list(copy.deepcopy(circle_set))

	# We cycle on the points on the circle that we slide on
	while circle_set:

		red_edge_temp = edges_to_go_through[-1]
		# We look for the right neighbour
		for (candidate_region, candidate_edge) in middle_region.red_neighbours:
			
			if candidate_edge == red_edge_temp:

				break 
		
		# We move in the new region
		middle_region = candidate_region

		# We append this region to the list of regions to go through
		regions_to_go_through.append(middle_region.label)

		# We identify the index of the edge that we entered from
		entering_index = get_index_of_edge(middle_region.input, red_edge_temp[::-1])

		# We use this index to indentify the new red edge that we need to cut through
		# Since we are keeping the blue circle that we are slinding on on the right,
		# we only need to take the second edge from the one that we entered from,
		# counting counter-clock wise

		new_index = (entering_index + 2) % middle_region.number_edges

		red_edge_temp = middle_region.input[new_index: new_index + 2]

		edges_to_go_through.append(red_edge_temp)

		# We remove the initial point of the new red edge to go through, which is 
		# a point on the blue circle that we are slinfing on
		circle_set.remove(red_edge_temp[0])


	# We create a dictionary for the output
	output = dict()

	output['regions_to_go_through'] = regions_to_go_through
	output['edges_to_go_through'] = edges_to_go_through
	output['edge_to_slide'] = edge_to_modify
	output['circle'] = circle_list
	
	return output