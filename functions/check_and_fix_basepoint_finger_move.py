import copy

def check_and_fix_basepoint_finger_move(diagram, region_label, edge_to_check, new_red_edge):
	if region_label in diagram.basepoint_regions_and_red_edges.keys():

		# The region has a basepoint, we check if it have modified the associated red edge
		if edge_to_check in diagram.basepoint_regions_and_red_edges[region_label]:
				
			# We put the new red edge in the list
			diagram.basepoint_regions_and_red_edges[region_label].append(new_red_edge)
			# We remove the old red edge
			diagram.basepoint_regions_and_red_edges[region_label].remove(edge_to_check)

			# We put in the updated information about the border component
			diagram.basepoint_regions_and_red_edges[tuple(new_red_edge)] = diagram.basepoint_regions_and_red_edges[tuple(edge_to_check)]
			# We eliminate the outdated information
			del diagram.basepoint_regions_and_red_edges[tuple(edge_to_check)]



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