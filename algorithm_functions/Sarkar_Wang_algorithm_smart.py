import sys
import copy

from algorithm_functions.finger_move import finger_move
from algorithm_functions.handle_slide import handle_slide
from algorithm_functions.find_the_best_move import find_the_best_move, exploring_the_neighbors
from algorithm_functions.generalized_handleslide_searcher import generalized_handleslide_searcher
from algorithm_functions.generalized_handle_slide import generalized_handle_slide
from algorithm_functions.compare_possible_diagrams import compare_possible_diagrams

from functions.get_index_of_edge import get_index_of_edge

#from classes.Heegaard_Diagram_class import Heegaard_diagram
import classes.Heegaard_Diagram_class

def Sarkar_Wang_algorithm_smart(diagram):

	# First off, we check the max distance complexity of the diagram.
	# If it is zero, then the diagram is nice and we can end the algorithm 

	if not diagram.distance_complexities:
		diagram.is_nice = True
	else:
		# We idenitfy the region that we want to modify
		bad_region_to_modify = diagram.distance_complexities[diagram.distance_diagram][-1][1]
		
		# Whatever the move, we'll start from this region
		starting_region_label = bad_region_to_modify.label
		
		# We find a neighbor region with stricly lesser distance
		for (neighbor, edge_to_modify) in bad_region_to_modify.blue_neighbors:
			if neighbor.distance < bad_region_to_modify.distance:
				break 
		
		# We understand which is the second red edge after edge_to_modify
		# To do so, we need the index of edge_to_modify in the bad region
		edge_to_modify_index = get_index_of_edge(bad_region_to_modify.input, edge_to_modify)


		'''
		# OLD VARIANT

		# We now go exploring the neighbors, pushing our finger through the rectangular regions and 
		# stopping if we finish in a non-rectangular region
		(last_region, edges_to_go_through, regions_to_go_through) = exploring_the_neighbors(bad_region_to_modify, first_red_edge_algorithm_index)
		'''


		# NEW VARIANT, VERSION 2: 
		# We try to find the best move to do. This means that we find all the possible moves of the 
		# algorithm and we select which ones makes the complexity goes down the most; among these we'll
		# choose the one that yields out the smallest number of generators

		# For now we only search for generalized handleslides, as they (if they exist) are the only moves
		# that can make the complexity goes down by a factor of 2
		possible_generalized_handleslides = generalized_handleslide_searcher(diagram, bad_region_to_modify.label, edge_to_modify, edge_to_modify_index)
	
		
		#'''


		# We now need to understand which move is the best one.
		# To do so, we try to apply them all and afterwards we count the number of generators
		# and we compare the total complexities




		# As first thing, we want to try the generalized handleslides
		# In fact, an handleslide is the only possibility to make the complexity to go down
		# by an even factor (in the sense that we can move a factor of badness 2 by the baddest region), 
		# therefore if we find such move, we don't need to try all the classic moves

		# We set all the dictionary that we'll need
		possible_future_diagrams = dict()
		number_generators = dict()
		total_complexities = dict()


		for key in possible_generalized_handleslides.keys():
			
			# We create a copy of the diagram and we save it in the 
			# possible_future_diagrams dictionary under the key 
			# ('generalized_handleslide', key)
			old_regions_input = copy.deepcopy(diagram.regions_input.copy())
			old_basepoints_dictionary = copy.deepcopy(diagram.basepoints_dictionary)
			possible_future_diagrams[('generalized_handleslide', key)] = classes.Heegaard_Diagram_class.Heegaard_diagram(diagram.number_intersection_points, diagram.number_border_points, old_regions_input, old_basepoints_dictionary, False)

			# We then take the data to operate the move
			starting_region_label = possible_generalized_handleslides[key]['starting_region_label']
			regions_to_go_through = possible_generalized_handleslides[key]['regions_to_go_through']
			edges_to_go_through = possible_generalized_handleslides[key]['edges_to_go_through']
			edge_to_slide = possible_generalized_handleslides[key]['edge_to_slide']


			# We update the diagram's attribute about what regions we are going to modify
			possible_future_diagrams[('generalized_handleslide', key)].last_diagram_regions_modified = [starting_region_label] + [edge_to_modify] + [regions_to_go_through] + [edges_to_go_through] + [starting_region_label, neighbor.label, 'Generalized handleslide']

			# And we do the move
			generalized_handle_slide(possible_future_diagrams[('generalized_handleslide', key)], starting_region_label, regions_to_go_through, edges_to_go_through, edge_to_slide)


			# We compute the number of generators for this new diagram
			# and we save it in the number_generators dictionary
			#print(f'\nComplexity and number of generators of this possible future, for key {('generalized_handleslide', key)}')
			number_generators[('generalized_handleslide', key)] = possible_future_diagrams[('generalized_handleslide', key)].number_of_generators

			# We save the total complexity in the total_complexities dictionary
			total_complexities[('generalized_handleslide', key)] = possible_future_diagrams[('generalized_handleslide', key)].total_complexity



		# We now try the classical moves on the diagram
			
		possible_moves = find_the_best_move(bad_region_to_modify, edge_to_modify_index)


		# We create the right number of copies of the diagram
		# we save them in the possible_future_diagrams dictionary
			
		for key in possible_moves:
			old_regions_input = copy.deepcopy(diagram.regions_input.copy())
			old_basepoints_dictionary = copy.deepcopy(diagram.basepoints_dictionary)
			possible_future_diagrams[key] = classes.Heegaard_Diagram_class.Heegaard_diagram(diagram.number_intersection_points, diagram.number_border_points, old_regions_input, old_basepoints_dictionary, False)


		# We try all the possible moves
		for key in possible_moves:
			
			# We extract the details of the move
			(last_region, edges_to_go_through, regions_to_go_through) = possible_moves[key]

			
			# We are now in a non-rectangular region; we must understand in which 
			# of the four algorithm's cases we are
			# Since in the very last case (subcase 4.2) we have to explore other possibility, we check as first thing if 
			# we are in Case 4, if we are in subcase 4.2 and in such case we cycle until we reach another case

			# Case 4:
			# 	we came back to the starting region
			if last_region.label == bad_region_to_modify.label:
				
				# We have two subcases. 
				# To distinguish them, we need the index of the last crossed edge from the starting region's perspective
				# and the index of the first crossed red edge
				last_edge_starting_region_index = get_index_of_edge(bad_region_to_modify.input, edges_to_go_through[-1][::-1])
				first_edge_to_go_through_index = get_index_of_edge(bad_region_to_modify.input, edges_to_go_through[0])
				
				# Subcase 4.1:
				# 	we have returned via an edge adjacent to the first edge
				difference_indicies_absolute_value = abs(last_edge_starting_region_index - first_edge_to_go_through_index)
				if (difference_indicies_absolute_value == bad_region_to_modify.number_edges - 2) or (difference_indicies_absolute_value  == 2):
					
					# In this case we'll do an handle slide in the second-to-last case of the next if statement.
					# We don't need to iterate the exploration, we don't do anything for now
					pass
				
				# Subcase 4.2:
				# 	we have returned via an edge not adjacent to the first edge
				else:

					# We have to iterate the exploration
					flag_good_case = False
					counter_new_index = 5

					# The second condition is a sanity chek as the algorithm should stop before exploring all 
					# the possibilities
					while (not flag_good_case) and (counter_new_index < bad_region_to_modify.number_edges):

						# We then understand the index of the first red edge to cut through
						first_edge_to_go_through_index = (edge_to_modify_index + counter_new_index) % bad_region_to_modify.number_edges

						# We now go exploring the neighbors, pushing our finger through the rectangular regions and 
						# stopping if we finish in a non-rectangular region
						(last_region, edges_to_go_through, regions_to_go_through) = exploring_the_neighbors(bad_region_to_modify, first_edge_to_go_through_index)

						# We need to check if we can end the loop or if we need to iterate again
						if last_region.label == bad_region_to_modify.label:
				
							# We have two subcases to distinguish from
							last_edge_starting_region_index = get_index_of_edge(bad_region_to_modify.input, edges_to_go_through[-1][::-1])

							# Subcase 4.1:
							# 	we have returned via an edge adjacent to the first edge
							if (last_edge_starting_region_index - first_edge_to_go_through_index) % bad_region_to_modify.number_edges == 2: # TO CHECK IF IT WORKS
								
								# In this case we'll do an handle slide in the second-to-last case of the next if statement.
								# We don't need to iterate the exploration, we don't do anything for now
								flag_good_case = True
							
							# Subcase 4.2:
							# 	we have returned via an edge not adjacent to the first edge
							else:

								# We have to iterate the exploration. We modify the flag and we increment the counter, 
								# so we'll explore starting from the next red edge
								flag_good_case = False
								counter_new_index = 2 + counter_new_index
						
						else:

							# We are in one of the first 3 cases, therefore we are in a good case
							flag_good_case = True


					# We exited the while cycle, so we should be in one of the good cases.
					# Sanity check: we control that we didn't finish the cycle because we ended the edge to explore
					if counter_new_index >= bad_region_to_modify.number_edges:
						sys.exit("Something is wrong: after arriving in Case 4.2, we have explored all the possibilities without stopping, making a whole loop in the starting region")
				
			else:

				# We are in one of the first three cases, therefore we can proceed with the algorithm
				pass



			


			# We are now in one of the viable cases. 
			# We understand in which one we are, so that we can operate the right move


			# Case 1: 
			# 	a bigon is reached
			if last_region.number_edges == 2:

				# In this case we do a finger move that ends in this bigon
				ending_region_label = last_region.label

				# We update the diagram's attribute about what regions we are going to modify
				possible_future_diagrams[key].last_diagram_regions_modified = [starting_region_label] + [edge_to_modify] + [regions_to_go_through] + [edges_to_go_through] + [ending_region_label, neighbor.label, 'Finger move']

				# We operate the move
				finger_move(possible_future_diagrams[key], starting_region_label, ending_region_label, regions_to_go_through, edges_to_go_through, edge_to_modify)


			# Case 2: 
			# 	a region with distance stricly lesser than the starting reagion is reached
			elif last_region.distance <= (bad_region_to_modify.distance - 1):

				# In this case we do a finger move that ends in this region
				ending_region_label = last_region.label

				# We update the diagram's attribute about what regions we are going to modify
				possible_future_diagrams[key].last_diagram_regions_modified = [starting_region_label] + [edge_to_modify] + [regions_to_go_through] + [edges_to_go_through] + [ending_region_label, neighbor.label, 'Finger move']

				# We operate the move
				finger_move(possible_future_diagrams[key], starting_region_label, ending_region_label, regions_to_go_through, edges_to_go_through, edge_to_modify)


			# Case 3:
			# 	a region with distance equal to the starting reagion is reached, but different to the starting region, is reached
			elif (last_region.distance == bad_region_to_modify.distance) and (last_region.label != bad_region_to_modify.label):
				
				# In this case we do a finger move that ends in this region
				ending_region_label = last_region.label

				# We update the diagram's attribute about what regions we are going to modify
				possible_future_diagrams[key].last_diagram_regions_modified = [starting_region_label] + [edge_to_modify] + [regions_to_go_through] + [edges_to_go_through] + [ending_region_label, neighbor.label, 'Finger move']

				# We operate the move
				finger_move(possible_future_diagrams[key], starting_region_label, ending_region_label, regions_to_go_through, edges_to_go_through, edge_to_modify)


			# Case 4:
			# 	we came back to the starting region.
			elif last_region.label == bad_region_to_modify.label:
				
				# We have two subcases. 
				# To distinguish them, we need to find the index of the last crossed edge from the starting region's perspective
				last_edge_starting_region_index = get_index_of_edge(bad_region_to_modify.input, edges_to_go_through[-1][::-1])

				# Subcase 4.1:
				# 	we have returned via an edge adjacent to the first edge
				difference_indicies_absolute_value = abs(last_edge_starting_region_index - first_edge_to_go_through_index)
				if (difference_indicies_absolute_value == bad_region_to_modify.number_edges - 2) or (difference_indicies_absolute_value  == 2):
					
					# In this case we do an handle slide

					# We update the diagram's attribute about what regions we are going to modify
					possible_future_diagrams[key].last_diagram_regions_modified = [starting_region_label] + [edge_to_modify] + [regions_to_go_through] + [edges_to_go_through] + [starting_region_label, neighbor.label, 'Handle slide']

					# We operate the move
					handle_slide(possible_future_diagrams[key], starting_region_label, regions_to_go_through, edges_to_go_through, edge_to_modify)
				
				# Subcase 4.2:
				# 	we have returned via an edge not adjacent to the first edge
				else:

					# This is a sanity check as we should not be here after iterating the exploration
					sys.exit("Something is wrong: the iteration of the exploration didn't work")
			
			# Sanity check
			else:
				sys.exit("Something is wrong: we are in a case not counted by the algorithm")

			
			# We compute the number of generators for this new diagram
			# and we save it in the number_generators dictionary
			number_generators[key] = possible_future_diagrams[key].number_of_generators

			# We save the total complexity in the total_complexities dictionary
			total_complexities[key] = possible_future_diagrams[key].total_complexity



		
		
		# We need to understan which diagram is better
		next_diagram = compare_possible_diagrams(diagram, possible_future_diagrams, total_complexities, number_generators)



		# We save the new diagram as diagram
		new_regions_input = copy.deepcopy(next_diagram.regions_input.copy())
		new_basepoints_dictionary = copy.deepcopy(next_diagram.basepoints_dictionary)
		new_last_regions_modified = copy.deepcopy(next_diagram.last_diagram_regions_modified)
		diagram.__init__(next_diagram.number_intersection_points, next_diagram.number_border_points, new_regions_input, new_basepoints_dictionary, new_last_regions_modified)