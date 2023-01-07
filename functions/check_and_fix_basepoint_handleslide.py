import copy
import sys

def check_and_fix_basepoint_handleslide_starting_region_first_edge(diagram, region_label, region_cutted_label, edge_to_slide_index, last_edge_index, edge_to_check, new_red_edge_starting_region, new_red_edge_starting_region_cutted):

	# We first check the first red edge
			
	if edge_to_check in diagram.basepoint_regions_and_red_edges[region_label]:
				
		# It is in the first edge, therefore we leave it in the remaining half of this edge

		# We need to distinguish in two cases
		if edge_to_slide_index < last_edge_index:

			# In this case the half edge of edges_to_go_through[0] is still in starting_region,
			# hence we only need to update this value in the dictionary

			# We put the new red edge in the list
			diagram.basepoint_regions_and_red_edges[region_label].append(new_red_edge_starting_region)
			# We remove the old red edge
			diagram.basepoint_regions_and_red_edges[region_label].remove(edge_to_check)


			# We put in the updated information about the border component
			diagram.basepoint_regions_and_red_edges[tuple(new_red_edge_starting_region)] = diagram.basepoint_regions_and_red_edges[tuple(edge_to_check)]
			# We eliminate the outdated information
			del diagram.basepoint_regions_and_red_edges[tuple(edge_to_check)]
			

		else:
			# Notice that this is always the case in the algorithm as it is presented by the original paper

			# In this case the half edge of edges_to_go_through[0] is in starting_region_cutted,
			# hence we remove edges_to_go_through[0] from the dictionary and we add the new red 
			# edge to the new entry for region_cutted

			# We add the new red edge
			diagram.basepoint_regions_and_red_edges[region_cutted_label].append(new_red_edge_starting_region_cutted)
			# We remove the old red edge
			diagram.basepoint_regions_and_red_edges[region_label].remove(edge_to_check)


			# We put in the updated information about the border component
			diagram.basepoint_regions_and_red_edges[tuple(new_red_edge_starting_region_cutted)] = diagram.basepoint_regions_and_red_edges[tuple(edge_to_check)]
			# We eliminate the outdated information
			del diagram.basepoint_regions_and_red_edges[tuple(edge_to_check)]
































def check_and_fix_basepoint_handleslide_starting_region_last_edge(diagram, region_label, region_cutted_label, edge_to_slide_index, last_edge_index, edge_to_check, new_red_edge_starting_region, new_red_edge_starting_region_cutted):

	# We check now the last red edge
		
	if edge_to_check in diagram.basepoint_regions_and_red_edges[region_label]:
			
		# We have a basepoint in the last edge, therefore we leave it in the remaining half of this edge

		# We need to distinguish in two cases
		if edge_to_slide_index < last_edge_index:

			# In this case the half edge of edges_to_go_through[-1][::-1] is in starting_region_cutted,
			# hence we remove edges_to_go_through[-1][::-1] from the dictionary and we remember that we
			# need to add it at the end of the handle slide operation (in this way we know the 
			# right label for starting_region_cutted) by setting the half_ending_edge_flag to True

			
			# We add the new red edge
			diagram.basepoint_regions_and_red_edges[region_cutted_label].append(new_red_edge_starting_region_cutted)
			# We remove the old red edge
			diagram.basepoint_regions_and_red_edges[region_label].remove(edge_to_check)	


			# We put in the updated information about the border component
			diagram.basepoint_regions_and_red_edges[tuple(new_red_edge_starting_region_cutted)] = diagram.basepoint_regions_and_red_edges[tuple(edge_to_check)]
			# We eliminate the outdated information
			del diagram.basepoint_regions_and_red_edges[tuple(edge_to_check)]		

		else:
			# Notice that this is always the case in the algorithm as it is presented by the original paper

			# In this case the half edge of edges_to_go_through[-1][::-1] is still in starting_region,
			# hence we only need to update this value in the dictionary

			# We put the new red edge in the list
			diagram.basepoint_regions_and_red_edges[region_label].append(new_red_edge_starting_region)
			# We remove the old red edge
			diagram.basepoint_regions_and_red_edges[region_label].remove(edge_to_check)


			# We put in the updated information about the border component
			diagram.basepoint_regions_and_red_edges[tuple(new_red_edge_starting_region)] = diagram.basepoint_regions_and_red_edges[tuple(edge_to_check)]
			# We eliminate the outdated information
			del diagram.basepoint_regions_and_red_edges[tuple(edge_to_check)]


































def check_if_red_edge_on_starting_region_cutted_handleslide(diagram, region_label, new_region_to_check, new_label):

	# We zip new_region_to_check
	new_region_to_check_zipped = list(map(list, zip(new_region_to_check, new_region_to_check[1:]+ [new_region_to_check[0]])))
	
	# We generate the red edges of new_region_to_check
	new_region_to_check_zipped_red_edges = new_region_to_check_zipped[0::2]

	# We create the new entry for new_region_to_check in the dictionary, if it doesn't exist already
	if new_label not in diagram.basepoint_regions_and_red_edges.keys():
		
		diagram.basepoint_regions_and_red_edges[new_label] = []

	# We create a copy of the list of red edges in diagram.basepoint_regions_and_red_edges[region_label],
	# so that we can iterate on it
	iteration_list = copy.deepcopy(diagram.basepoint_regions_and_red_edges[region_label])

	# We check if we have indeed moved any red edges with basepoint that was in region to new_region_to_check
	for red_edge in iteration_list:

		if red_edge in new_region_to_check_zipped_red_edges:

			# If it is moved, we append it to the new list
			diagram.basepoint_regions_and_red_edges[new_label].append(red_edge)
			
			# And we remove it from the old list
			diagram.basepoint_regions_and_red_edges[region_label].remove(red_edge)

























def check_and_fix_basepoint_handleslide(diagram, region_label, middle_region, entering_edge, exiting_edge, number_intersection_points):

	# If the region has a basepoint, we check if it have modified the associated red edge
	# We want to leave the basepoint distant from the inner blue circle that we slide on.
	# This means to put it on the half red edge remaining in "middle_region" by construction
	

	if region_label in diagram.basepoint_regions_and_red_edges.keys():

		# The region has a basepoint, we check if we have modified the associated red edge
		# We place the new basepoint in middle_region, as by construction middle_region_cutted is the rectangle obtained from the handleslide
		
		# We check if the edge from which we are entering has a basepoint
		if entering_edge in diagram.basepoint_regions_and_red_edges[region_label]:
			
			# We need to understand which is the new red_edge
			index_intersection_point_entering = middle_region.index(number_intersection_points - 1)

			if index_intersection_point_entering % 2== 0:

				# The new entering edge is [number_intersection_points - 1, entering_edge[1]]
				new_entering_edge = [number_intersection_points - 1, entering_edge[1]]

				
				# Sanity check
				if middle_region[index_intersection_point_entering + 1] != entering_edge[1]:
					
					sys.exit('Error: we messed up while trying to fix the basepoints during an handleslide, we did not get the right new entering edge')

			else:

				# The new entering edge is [entering_edge[0], number_intersection_points - 1]
				new_entering_edge = [entering_edge[0], number_intersection_points - 1]
				
				# Sanity check
				if middle_region[index_intersection_point_entering-1] != entering_edge[0]:
					
					sys.exit('Error: we messed up while trying to fix the basepoints during an handleslide, we did not get the right new entering edge')


			# We append the new red_edge to the list with middle_region as key
			diagram.basepoint_regions_and_red_edges[region_label].append(new_entering_edge)
			# And we remove the previous red edge
			diagram.basepoint_regions_and_red_edges[region_label].remove(entering_edge)


			# We put in the updated information about the border component
			diagram.basepoint_regions_and_red_edges[tuple(new_entering_edge)] = diagram.basepoint_regions_and_red_edges[tuple(entering_edge)]
			# We eliminate the outdated information
			del diagram.basepoint_regions_and_red_edges[tuple(entering_edge)]
		
		else:
		
			pass


		# We check if the edge from which we are exiting has a basepoint
		if exiting_edge in diagram.basepoint_regions_and_red_edges[region_label]:

			# We need to understand which is the new red_edge
			index_intersection_point_exiting = middle_region.index(number_intersection_points)

			if index_intersection_point_exiting % 2== 0:

				# The new exiting edge is [number_intersection_points, exiting_edge[1]]
				new_exiting_edge = [number_intersection_points, exiting_edge[1]]

				
				# Sanity check
				if middle_region[index_intersection_point_exiting + 1] != exiting_edge[1]:
					
					sys.exit('Error: we messed up while trying to fix the basepoints during an handleslide, we did not get the right new exiting edge')

			else:

				# The new exiting edge is [exiting_edge[0], number_intersection_points]
				new_exiting_edge = [exiting_edge[0], number_intersection_points]
				
				# Sanity check
				if middle_region[index_intersection_point_exiting-1] != exiting_edge[0]:
					
					sys.exit('Error: we messed up while trying to fix the basepoints during an handleslide, we did not get the right new exiting edge')
										
			# We append the new red_edge to the list with middle_region as key
			diagram.basepoint_regions_and_red_edges[region_label].append(new_exiting_edge)
			# And we remove the previous red edge
			diagram.basepoint_regions_and_red_edges[region_label].remove(exiting_edge)


			# We put in the updated information about the border component
			diagram.basepoint_regions_and_red_edges[tuple(new_exiting_edge)] = diagram.basepoint_regions_and_red_edges[tuple(exiting_edge)]
			# We eliminate the outdated information
			del diagram.basepoint_regions_and_red_edges[tuple(exiting_edge)]
		

		else:
			
			pass























def check_if_red_edge_on_new_region_cutted(diagram, region_label, new_region_to_check, new_label):

	if region_label in diagram.basepoint_regions_and_red_edges.keys():
			
			# We zip new_region_to_check
			new_region_to_check_zipped = list(map(list, zip(new_region_to_check, new_region_to_check[1:]+ [new_region_to_check[0]])))
			
			# We generate the red edges of new_region_to_check
			new_region_to_check_zipped_red_edges = new_region_to_check_zipped[0::2]

			# We create the new entry for new_region_to_check in the dictionary
			diagram.basepoint_regions_and_red_edges[new_label] = []

			# We create a copy of the list of red edges in diagram.basepoint_regions_and_red_edges[region_label],
			# so that we can iterate on it
			iteration_list = copy.deepcopy(diagram.basepoint_regions_and_red_edges[region_label])

			# We check if we have indeed moved any red edges with basepoint that was in region to new_region_to_check
			for red_edge in iteration_list:

				if red_edge in new_region_to_check_zipped_red_edges:

					# If it is moved, we append it to the new list
					diagram.basepoint_regions_and_red_edges[new_label].append(red_edge)
					
					# And we remove it from the old list
					diagram.basepoint_regions_and_red_edges[region_label].remove(red_edge)



















































def check_and_fix_basepoint_generalized_handleslide(diagram, region_label, entering_edge, exiting_edge, new_entering_edge, new_exiting_edge):

	# If the region has a basepoint, we check if it have modified the associated red edge
	# We want to leave the basepoint distant from the inner blue circle that we slide on,
	# for the first region this means to decide if we have to put it on the half red edge 
	# remaining in "starting_region_cutted" or in the half red edge in "starting_region"
	# (recall that we do an handleslide only if the first edge that we go through and the 
	# last edge that we go through are separate only by one blue edge
	

	if region_label in diagram.basepoint_regions_and_red_edges.keys():

		# The region has a basepoint, we check if we have modified the associated red edge
			
		
		# By construction, there is no intersection between middle_region and inner_circle, 
		# therefore we place the new basepoint on the correspondant half red edge in middle_region


		

		# As first check, we want to see if we are modifying a bigon
		# In such case, we do a separate construction
		if entering_edge == exiting_edge:

			# We check if the red edge of the bigon has a basepoint
			if entering_edge in diagram.basepoint_regions_and_red_edges[region_label]:

				# We don't need to distinguish two cases since it doesn't change the new red edge
											
				# We append the new red_edge to the list with middle_region as key
				diagram.basepoint_regions_and_red_edges[region_label].append(new_entering_edge)
				# And we remove the previous red edge
				diagram.basepoint_regions_and_red_edges[region_label].remove(entering_edge)


				# We put in the updated information about the border component
				diagram.basepoint_regions_and_red_edges[tuple(new_entering_edge)] = diagram.basepoint_regions_and_red_edges[tuple(entering_edge)]
				# We eliminate the outdated information
				del diagram.basepoint_regions_and_red_edges[tuple(entering_edge)]



		else:

			# We are not modifying a bigon, therefore we cand o a more general construction

			# We check if the edge from which we are entering has a basepoint
			if entering_edge in diagram.basepoint_regions_and_red_edges[region_label]:
				# We don't need to distinguish two cases since it doesn't change the new red edge
											
				# We append the new red_edge to the list with middle_region as key
				diagram.basepoint_regions_and_red_edges[region_label].append(new_entering_edge)
				# And we remove the previous red edge
				diagram.basepoint_regions_and_red_edges[region_label].remove(entering_edge)


				# We put in the updated information about the border component
				diagram.basepoint_regions_and_red_edges[tuple(new_entering_edge)] = diagram.basepoint_regions_and_red_edges[tuple(entering_edge)]
				# We eliminate the outdated information
				del diagram.basepoint_regions_and_red_edges[tuple(entering_edge)]
			
			else:
			
				pass


			# We check if the edge from which we are exiting has a basepoint
			if exiting_edge in diagram.basepoint_regions_and_red_edges[region_label]:

				# We don't need to distinguish two cases since it doesn't change the new red edge
											
				# We append the new red_edge to the list with middle_region as key
				diagram.basepoint_regions_and_red_edges[region_label].append(new_exiting_edge)
				# And we remove the previous red edge
				diagram.basepoint_regions_and_red_edges[region_label].remove(exiting_edge)


				# We put in the updated information about the border component
				diagram.basepoint_regions_and_red_edges[tuple(new_exiting_edge)] = diagram.basepoint_regions_and_red_edges[tuple(exiting_edge)]
				# We eliminate the outdated information
				del diagram.basepoint_regions_and_red_edges[tuple(exiting_edge)]
			

			else:
				
				pass