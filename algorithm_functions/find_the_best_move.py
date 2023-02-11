import copy

from functions.get_index_of_edge import get_index_of_edge



def find_the_best_move(bad_region_to_modify, edge_to_modify_index):

	# We create a dictionary to save all the possibilities
	possible_moves = dict()

	# We create a list of all the possible red edges that we can go out from the bad region
	red_edges_bad_region = copy.deepcopy(bad_region_to_modify.red_edges)

	# We then try all the possibilities
	while red_edges_bad_region:

		red_edge = red_edges_bad_region[0]

		red_edge_index = get_index_of_edge(bad_region_to_modify.input, red_edge)

		# If the red edge is the one immediately after the blue edge that we are modifying
		# or the one immediately before, the only possible move that we can do is an 
		# handleslide (in fact, a fingermove would not reduce the badness of the region)
		# We check if we are in this case and we set a flag to keep track of it
		only_handleslide_allowed = False

		if ((edge_to_modify_index - red_edge_index) == 1) or ((edge_to_modify_index - red_edge_index) == (-1 % bad_region_to_modify.number_edges)) or ((edge_to_modify_index - red_edge_index) == -1):
			only_handleslide_allowed = True


		# We explore going out from red_edge
		(last_region, edges_to_go_through, regions_to_go_through) = exploring_the_neighbours(bad_region_to_modify, red_edge_index)

		

		# We understand if it is an handleslide. In such case, we need to do some 
		# checks to see if it is an admitted handleslide
		if last_region.label == bad_region_to_modify.label:

			# We understand if we came back from an adjacent edge, if not we 
			# don't save this move
			last_edge_starting_region_index = get_index_of_edge(bad_region_to_modify.input, edges_to_go_through[-1][::-1])
			
			# Subcase 4.1:
			# we have returned via an edge adjacent to the first edge (but the 
			# blue edge that we modify is not in the middle of them)
			difference_indicies_absolute_value = abs(last_edge_starting_region_index - red_edge_index)
			
			# Even if the difference between indicies of the first red edge and the last red edge is 2, we need to make sure that 
			# they don't have the edge that we are modifying as blue edge between them.
			# To do so, we set two flags, is_blue_edge_middle_1 and is_blue_edge_middle_2, that check if this is the case
			is_blue_edge_middle_1 = (last_edge_starting_region_index + 1 % bad_region_to_modify.number_edges == edge_to_modify_index) and (edge_to_modify_index + 1 % bad_region_to_modify.number_edges == red_edge_index)
			is_blue_edge_middle_2 = (red_edge_index + 1 % bad_region_to_modify.number_edges == edge_to_modify_index) and (edge_to_modify_index + 1 % bad_region_to_modify.number_edges == last_edge_starting_region_index)
			
			
			is_blue_edge_middle = is_blue_edge_middle_1 or is_blue_edge_middle_2

			if (difference_indicies_absolute_value == bad_region_to_modify.number_edges - 2) or (difference_indicies_absolute_value  == 2):
				
				if not is_blue_edge_middle:

					# We save everything in the dictionary, using red_edge as key 
					possible_moves[tuple(red_edge)] = [last_region, edges_to_go_through, regions_to_go_through]

					# We remove the last red edge from the list of red edges on which we are iterating, as it
					# would yield the same move backward
					red_edges_bad_region.remove(edges_to_go_through[-1][::-1])

				else:
					# This is a wrong handleslide, hence we don't save it
					pass

			else:

				# This is a wrong handleslide, hence we don't save it
				pass
		
		elif only_handleslide_allowed:

			# We found a fingermove which is not allowed, as the only_handleslide_allowed
			# flag is set to True. Therefore we can't save this move
			pass

		else:
			# We have found a fingermove which is allowed. We save this move in the dictionary, 
			# using the first red_edge as key 
			possible_moves[tuple(red_edge)] = [last_region, edges_to_go_through, regions_to_go_through]


		# We remove red_edge from the list of red edges to analyze
		red_edges_bad_region.remove(red_edge)

	return possible_moves





def exploring_the_neighbours(bad_region_to_modify, first_edge_to_go_through_index):

	# We understand the region that is neighbour to bad_region_to_modify via first_edge_to_go_through
	# (i.e. we understand which is the first region in which we go)
	for (first_region, first_edge) in bad_region_to_modify.red_neighbours:
		if first_edge == bad_region_to_modify.input[first_edge_to_go_through_index:first_edge_to_go_through_index+2]:
			break

	# We create the lists of edges and regions to cut
	edges_to_go_through = [bad_region_to_modify.input[first_edge_to_go_through_index:first_edge_to_go_through_index+2]]
	regions_to_go_through = [first_region.label]



	# We now push the move through square regions and we stop in any other case
	middle_region = first_region
		
	while (middle_region.number_edges == 4) and (middle_region.distance >= bad_region_to_modify.distance):

		# We find the next region and the next edge
		for (next_region, next_edge) in middle_region.red_neighbours:
			if next_edge != edges_to_go_through[-1][::-1]:
				break
			
		# We append the edge in the lists of edges to go through and we proceed
		edges_to_go_through.append(next_edge)
		regions_to_go_through.append(next_region.label)

		# We move in this new region
		middle_region = next_region

	# We cut off the last region added to regions_to_go_through, since we don't want it in the list in any case
	return (middle_region, edges_to_go_through, regions_to_go_through[:-1])







def find_handleslide(diagram, bad_region_to_modify, first_red_edge_algorithm_index, edge_to_modify_index):

	# We create a dictionary to save all the possibilities
	possible_moves = dict()

	# We set a general flag to know if we found at least one handleslide
	there_is_handleslide = False

	# We find the red_edge indicated by the algorithm
	red_edge_algorithm = bad_region_to_modify.input[first_red_edge_algorithm_index: first_red_edge_algorithm_index + 2]


	# We then try all the possibilities
	for red_edge in bad_region_to_modify.red_edges:


		red_edge_index = get_index_of_edge(bad_region_to_modify.input, red_edge)
		# We explore going out from red_edge
		(last_region, edges_to_go_through, regions_to_go_through) = exploring_the_neighbours(bad_region_to_modify, red_edge_index)

		# We check if this is the move that the algorithm would do
		if red_edge == red_edge_algorithm:
			algorithm_move = (last_region, edges_to_go_through, regions_to_go_through)

		# We understand if it is an handleslide
		if last_region.label == bad_region_to_modify.label:

			# We understand if we came back from an adjacent edge, if not we 
			# don't save this move
			last_edge_starting_region_index = get_index_of_edge(bad_region_to_modify.input, edges_to_go_through[-1][::-1])
			
			# Subcase 4.1:
			# we have returned via an edge adjacent to the first edge (but the blue edge that we modify is not in the middle of them)
			difference_indicies_absolute_value = abs(last_edge_starting_region_index - red_edge_index)

			# Even if the difference between indicies of the first red edge and the last red edge is 2, we need to make sure that 
			# they don't have the edge that we are modifying as blue edge between them.
			# To do so, we set two flags, is_blue_edge_middle_1 and is_blue_edge_middle_2, that check if this is the case
			is_blue_edge_middle_1 = (last_edge_starting_region_index + 1 % bad_region_to_modify.number_edges == edge_to_modify_index) and (edge_to_modify_index + 1 % bad_region_to_modify.number_edges == red_edge_index)
			is_blue_edge_middle_2 = (red_edge_index + 1 % bad_region_to_modify.number_edges == edge_to_modify_index) and (last_edge_starting_region_index + 1 % bad_region_to_modify.number_edges == red_edge_index)
			
			
			is_blue_edge_middle = is_blue_edge_middle_1 or is_blue_edge_middle_2

			if (difference_indicies_absolute_value == bad_region_to_modify.number_edges - 2) or (difference_indicies_absolute_value  == 2):
				
				if not is_blue_edge_middle:

					handle_slide_flag = True
					there_is_handleslide = True

					# We count the lenght of the move
					lenght_move = len(regions_to_go_through)

					# We save everything in the dictionary, using the first red_edge 
					# and the lenght of the move as keys 
					possible_moves[(tuple(red_edge), lenght_move)] = [handle_slide_flag, last_region, edges_to_go_through, regions_to_go_through]

				else:
					# This is a wrong handleslide, hence we don't save it
					pass

			else:

				# This is a wrong handleslide, hence we don't save it
				pass

		else:
			handle_slide_flag = False

			# We count the lenght of the move
			lenght_move = len(regions_to_go_through)

			# We save everything in the dictionary, using the first red_edge 
			# and the lenght of the move as keys 
			possible_moves[(tuple(red_edge), lenght_move)] = [handle_slide_flag, last_region, edges_to_go_through, regions_to_go_through]

	
	if there_is_handleslide:

		# We assign a fake impossible lenght of the move to be able to 
		# find the shorter handleslide

		len_temp = len(diagram.regions_input) + 3

		for key in possible_moves.keys():

			# We check that it is an handleslide and that the lenght is less than
			# the lenght af the handleslide that we are considering
			if (possible_moves[key][0] == True) and (key[1] <= len_temp):

				best_move_key = key
				len_temp = key[1]
		
		last_region = possible_moves[best_move_key][1]
		edges_to_go_through = possible_moves[best_move_key][2]
		regions_to_go_through= possible_moves[best_move_key][3]


		return (last_region, edges_to_go_through, regions_to_go_through)

	else:

		# We return the move that the algoithm would have done
		return algorithm_move