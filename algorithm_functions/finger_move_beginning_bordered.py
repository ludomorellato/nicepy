import sys

from algorithm_functions.finger_move import finger_move




def finger_move_beginning_bordered(diagram, user_experience):

	print("\n")
	print("We check if the diagram is bordered and, in such case, if some initial finger moves are needed to fix the border regions\n")

	if user_experience:
		input('\nPress enter to continue...')
		print("\n")

	if diagram.number_border_points == 0:
		# If we are in a non-border diagram, then we don't need to do this beginning move
		print("The diagram is not bordered, therefore we don't need to do these fixing moves\n")

		if user_experience:
			input('\nPress enter to continue...')
		
		return None

	else:

		# If we have a border diagram, we need to check if the beginnning move is needed

		something_to_do = False
		regions_to_fix = []

		for i in diagram.border_regions:
			region = diagram.regions[i]
			if (region.badness > 0) and (region.distance > 0):
				something_to_do = True
				regions_to_fix.append(i)
		

		if something_to_do:
			# A finger move to fix the diagram is required for the regions
			# in regions_to_fix, we fix them

			
			print('The diagram is bordered and we need to fix the border region')
			print('Now the required finger moves are going to be done')

			if user_experience:
				input('\nPress enter to continue...')
				print("\n")

			# We create a dictionary and a counter to keep track of the finger moves done on the diagram
			number_initial_finger_moves = 0
			intermediate_steps_beginning = dict()
			intermediate_steps_beginning[0] = (diagram.number_intersection_points, diagram.number_border_points, diagram.regions_input, diagram.basepoints_dictionary, [])


			while regions_to_fix:

				number_initial_finger_moves = 1 + number_initial_finger_moves

				# We take the first region to fix and we indentify the first left "neighbour" with the basepoint
				region_temp = regions_to_fix[0]
				edges_already_crossed = []
				regions_crossed = [region_temp]
				

				while region_temp not in diagram.multiplicity_zero_regions:

					# We always want to search the starting region to do the finger move in a clock-wise (wrt the border)
					# direction. We then need to see which is the "upper" border_point of the region from which we start;
					# to do so, we only need to compute the "max -1" of the intersection between the input of the region 
					# and the border points (in fact, we required to go counter clock-wise with the labelling of the 
					# border points on a border component).
					# The minimum wouldn't work as we may have more than one border edge and if we take the minimum we may
					# skip some "interior region".
					# We create a list for the intersection between the intersection points of the region and the border points,
					# then we compute the maximum -1 of this list
					border_points_region_temp = [point for point in diagram.regions[region_temp].input if point in list(range(1, diagram.number_border_points + 1))]
					upper_intersection_point = max(border_points_region_temp) - 1

					for [potential_neighbour, edge_crossed] in diagram.regions[region_temp].red_neighbours:

						# We check that the edge that we crossed is indeed the "upper edge" of our region
						is_upper_border_region = (min(edge_crossed) == upper_intersection_point)

						# Maybe this is not required anymore.
						# We check that we are not going back (but notice that we can be going for a second time 
						# in the same region if such region has more than one border edge on the same border component)
						is_new_edge = (edge_crossed not in edges_already_crossed)

						if (is_new_edge) and (is_upper_border_region):

							# If the condition are satisfied, then we go in this new region, we 
							# update the values and we break the for cycle
							edges_already_crossed.append(edge_crossed)
							regions_crossed.append(potential_neighbour.label)
							region_temp = potential_neighbour.label
							break
				
				

				# We are now in a region with basepoint and we want to do a finger move from this region to another region
				# with a basepoint (not necessarly the same region), going counter clock-wise.
				# We then rearrange the labels already found and we start to find this new region on the other side


				regions_crossed = regions_crossed[::-1]
				edges_already_crossed = [edge[::-1] for edge in edges_already_crossed[::-1]]

				# We start again from the very first region that we had, the one that needs fixing
				region_temp = regions_crossed[-1]

				# As before we need to check that we are going in the right direction. In this second part, 
				# we want to cross the very lower border-edge of this region (since it is "the only" border edge of 
				# this region that we havent' touchted), but for all the other region we want to do a similar thing as above. 
				# Thereforewe set here the first lower_intersection_point, and then we change it at the end of the cycle for 
				# the other regions
				# We create a list for the intersection between the intersection points of the region and the border points,
				# then we compute the maximum of this list
				border_points_region_temp = [point for point in diagram.regions[region_temp].input if point in list(range(1, diagram.number_border_points + 1))]
				lower_intersection_point = max(border_points_region_temp)
				

				while region_temp not in diagram.multiplicity_zero_regions:
					
					for [potential_neighbour, edge_crossed] in diagram.regions[region_temp].red_neighbours:

						# We check that the edge that we crossed is indeed the "lower edge" of our region
						is_lower_border_region = (min(edge_crossed) == lower_intersection_point)

						# Maybe this is not required anymore.
						# We check that we are not going back (but notice that we can be going for a second time 
						# in the same region if such region has more than one border edge on the same border component)
						is_new_edge = (edge_crossed not in edges_already_crossed)

						if (is_new_edge) and (is_lower_border_region):

							# If the condition are satisfied, then we go in this new region, we 
							# update the values and we break the for cycle
							edges_already_crossed.append(edge_crossed)
							regions_crossed.append(potential_neighbour.label)
							region_temp = potential_neighbour.label
							break
					

					# As we said above, now we change the lower_intersection_point that we'll use for the next cycle
					lower_intersection_point = min(diagram.regions[region_temp].input) + 1


				# We are almost ready to do the finger move, this is what we know
				starting_region = regions_crossed[0]
				ending_region = regions_crossed[-1]
				regions_to_go_through = regions_crossed[1:-1]
				edges_to_go_through = edges_already_crossed


				# Now we only need to understand on which edge we want to do the finger move.
				# We want to take the blue edge right after the first red edge that we cross
				# (which is the blue edge right to the left of such red arc).
				end_point_blue_edge = max(edges_already_crossed[0])
				for potential_edge in diagram.regions[starting_region].blue_edges:
					if end_point_blue_edge == potential_edge[1]:
						break


				edge_to_bend = potential_edge


				# We now prepare the setting to do the finger move on all the regions found between 
				# starting_region and ending_region 
				
				# First, we remove the fixed regions from the list of regions to fix
				regions_to_fix = [region for region in regions_to_fix if region not in regions_to_go_through]

				# We recover now the neighbour region that has the bent edge (just to know it for the "last_diagrams_regions_modified" attribute)
				neighbour_region = False
				for [candidate_region, edge] in diagram.regions[starting_region].blue_neighbours:
					if edge == edge_to_bend:
						neighbour_region = candidate_region
						break
				
				neighbour_region_label = neighbour_region.label

				# We add the diagram's attribute that tell us what we have changed from the previous diagram 
				diagram.last_diagram_regions_modified = [starting_region] + [edge_to_bend] + [regions_to_go_through] + [edges_to_go_through] + [ending_region, neighbour_region_label, 'Finger move']

				# We now update the diagram doing the finger move
				finger_move(diagram, starting_region, ending_region, regions_to_go_through, edges_to_go_through, edge_to_bend)

				# We save the new diagram in the intermediate_steps dictionary
				intermediate_steps_beginning[number_initial_finger_moves] = (diagram.number_intersection_points, diagram.number_border_points, diagram.regions_input, diagram.basepoints_dictionary, diagram.last_diagram_regions_modified)



			# We remove the "previous_moves" attribute to our diagram as we don't want them to
			# appear in in the zeroth step of the algorithm
			diagram.last_diagram_regions_modified = []

			# We put in the dictionary the data of the numbers of finger moves done
			intermediate_steps_beginning['number_finger_moves'] = number_initial_finger_moves

			# We return the dictionary with the chenges
			return intermediate_steps_beginning				


		else:
			# All the border regions are good or they have distance 0,
			# we don't have anything to do.
			print("The diagram is bordered, but there is nothing to do with the border regions. We can proceed with the algorithm\n")
			
			if user_experience:
				input('\nPress enter to continue...')
				print("\n")
			
			return None