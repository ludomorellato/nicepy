import sys
import copy

from functions.get_index_of_edge import get_index_of_edge
from functions.check_and_fix_basepoint_handleslide import check_and_fix_basepoint_handleslide_starting_region_first_edge, check_and_fix_basepoint_handleslide_starting_region_last_edge, check_if_red_edge_on_starting_region_cutted_handleslide, check_and_fix_basepoint_generalized_handleslide, check_if_red_edge_on_new_region_cutted

# This function is quite similar to the one for the finger move.
# Howeverl notice that in this case we always have that starting and ending regions coincide.

# This function take as input a diagram, a starting (and ending) region, the regions
# through which we want to pass, the edges that we cut  (recall that they are always red edges)
# and the blue edge on which we operate the handle slide, called "edge_to_slide".
# As a result, we update the Heegaard Diagram to the new version.



def generalized_handle_slide(diagram, starting_region_label, regions_to_go_through, edges_to_go_through, edge_to_slide):


	edges_to_go_through = edges_to_go_through[:-1]
	regions_input = copy.deepcopy(diagram.regions_input)
	number_intersection_points = diagram.number_intersection_points
	diagram.NEW_number_intersection_points = diagram.number_intersection_points + len(edges_to_go_through)

	# From now on, all the modifications are going to be done on the regions_input list, so that we are going 
	# to take in account all the previous changes when we do a modification 
	

	# Before the modifications on the regions, we need (in the case of multiple visits) to copy 
	# the entering and exiting edges of each visit in a dictionary, in a way that
	# we can correct these edges internally for the future visits.
	# Notice that we can't do this in the edges_to_go_through list, otherwise we would 
	# encounter problems in the modification of the next regions (since those regions red
	# edges wouldn't match the red edges in edges_to_go_through anymore)
	internal_edges_dictionary = dict()

	# We fix by hand the first and the last edge

	# First edge
	internal_edges_dictionary[-1] = dict()
	internal_edges_dictionary[-1]['exiting_edge'] = copy.deepcopy(edges_to_go_through[0])
	
	# Last edge
	internal_edges_dictionary[len(edges_to_go_through)-1] = dict()
	internal_edges_dictionary[len(edges_to_go_through)-1]['entering_edge'] = copy.deepcopy(edges_to_go_through[-1][::-1])


	# We iterate on the others
	for index in range(len(edges_to_go_through)-1):
		
		# We create an entry in the dictionary under the key "index", in which we save the 
		# entering and the exiting edge
		internal_edges_dictionary[index] = dict()
		internal_edges_dictionary[index]['entering_edge'] = copy.deepcopy(edges_to_go_through[index][::-1])
		internal_edges_dictionary[index]['exiting_edge'] = copy.deepcopy(edges_to_go_through[index + 1])






	# We can now start to modify the regions in regions_input


	# We first fix the neighbour region with the slid edge and we cut the starting region in two
	# Remark that we may pass again through starting_region, but at that point we can treat it as if
	# it was a region in the middle of the move 
	# As intersection points, we add the first and the last, as we would do if we were to do it by hand

	# We need to set in a better way starting_region
	starting_region = regions_input[starting_region_label - 1]

	# We recover the index of the first edge to go through
	first_edge_index = get_index_of_edge(starting_region, internal_edges_dictionary[-1]['exiting_edge'])
	

	# We rewrite the input of the starting region in a way that the first edge is the first edge to 
	# go through with the handle slide (and we assign the right index to first_edge_index)
	starting_region = starting_region[first_edge_index: ] + starting_region[: first_edge_index]
	first_edge_index = 0

	# We now compute also the other two indices that we need from the starting region, i.e. the one 
	# of the last edge that we go through and the one of the edge to slide
	last_edge_index = get_index_of_edge(starting_region, internal_edges_dictionary[len(edges_to_go_through)-1]['entering_edge'])
	edge_to_slide_index = get_index_of_edge(starting_region, edge_to_slide)
	


	# We recover now the neighbour region that has the slid edge
	neighbour_region = False
	for [candidate_region, edge] in diagram.regions[starting_region_label].blue_neighbours:
		if edge == edge_to_slide:
			neighbour_region = candidate_region
			break
	
	neighbour_region_input = regions_input[neighbour_region.label - 1]

	# And we find the index of such edge for this region
	edge_to_fix_neighbour_index = get_index_of_edge(neighbour_region_input, edge_to_slide[::-1])
	

	# We then modify the neighbour region in the regions_input
	if edge_to_slide_index < last_edge_index:
		new_neighbour_region = neighbour_region_input[0: edge_to_fix_neighbour_index + 1] + [number_intersection_points + len(edges_to_go_through)] + starting_region[last_edge_index + 1:] + [starting_region[0], number_intersection_points + 1] + neighbour_region_input[edge_to_fix_neighbour_index + 1:]
		starting_region_cutted = starting_region[edge_to_slide_index + 1: last_edge_index + 1] + [number_intersection_points + len(edges_to_go_through)]
		starting_region = [number_intersection_points + 1] + starting_region[1:edge_to_slide_index + 1]

	else:
		new_neighbour_region = neighbour_region_input[0: edge_to_fix_neighbour_index + 1] + [number_intersection_points + 1] + starting_region[1:last_edge_index+1] + [number_intersection_points + len(edges_to_go_through)] + neighbour_region_input[edge_to_fix_neighbour_index + 1:]
		starting_region_cutted = [starting_region[0]] + [number_intersection_points + 1] + starting_region[edge_to_slide_index + 1:]
		starting_region = [number_intersection_points + len(edges_to_go_through)] + starting_region[last_edge_index + 1: edge_to_slide_index + 1]


	
	# We modify the input in the regions_input
	regions_input[neighbour_region.label -1] = new_neighbour_region
	regions_input[starting_region_label -1] = starting_region
	regions_input.append(starting_region_cutted)
	
	# We save the label of the cutted region, which can be helpful later
	starting_region_cutted_label = len(regions_input)
	


	# For diagrams of 4-ended tangles:
	# We check if starting_region is a region with basepoint in the case in which we have
	# closed the surface
	
	if diagram.is_tangle_diagram:

		if starting_region_label in diagram.basepoint_regions_and_red_edges.keys():

			# If the region has a basepoint, we check if it have modified the associated red edge
			# We want to leave the basepoint distant from the inner blue circle that we slide on,
			# for the first region this means to decide if we have to put it on the half red edge 
			# remaining in "starting_region_cutted" or in the half red edge in "starting_region"
			# (recall that we do an handleslide only if the first edge that we go through and the 
			# last edge that we go through are separate only by one blue edge
			

			# We create the new entry for starting_region_cutted in the basepoint dictionary,
			# it will eventually remain empty
			diagram.basepoint_regions_and_red_edges[starting_region_cutted_label] = []



			
			# We check the entering edge

			# We need to distinguish between two cases: if the next region is a bigon or not
			is_first_region_bigon = diagram.regions[regions_to_go_through[0]].number_edges == 2

			if is_first_region_bigon:
				
				# In this case we have that the new edges are formed only by new intersection points
				new_red_edge_exit_starting_region = [number_intersection_points + 1, number_intersection_points + 2]
				new_red_edge_exit_starting_region_cutted = [number_intersection_points + 2, number_intersection_points + 1]

			else:

				new_red_edge_exit_starting_region = [number_intersection_points + 1, edges_to_go_through[0][1]]
				new_red_edge_exit_starting_region_cutted = [edges_to_go_through[0][0], number_intersection_points + 1]


			check_and_fix_basepoint_handleslide_starting_region_first_edge(diagram, starting_region_label, starting_region_cutted_label, edge_to_slide_index, last_edge_index, edges_to_go_through[0], new_red_edge_exit_starting_region, new_red_edge_exit_starting_region_cutted)






			# We check the exiting edge

			# We need to distinguish between two cases: if the next region is a bigon or not
			is_last_region_bigon = diagram.regions[regions_to_go_through[-2]].number_edges == 2

			if is_last_region_bigon:
				
				# In this case we have that the new edges are formed only by new intersection points
				new_red_edge_enter_starting_region = [number_intersection_points + len(edges_to_go_through), number_intersection_points + len(edges_to_go_through) - 1]
				new_red_edge_enter_starting_region_cutted = [number_intersection_points + len(edges_to_go_through) - 1, number_intersection_points + len(edges_to_go_through)]

			else:

				new_red_edge_enter_starting_region = [number_intersection_points + len(edges_to_go_through), edges_to_go_through[0][0]]
				new_red_edge_enter_starting_region_cutted = [edges_to_go_through[-1][1], number_intersection_points + len(edges_to_go_through)]


			check_and_fix_basepoint_handleslide_starting_region_last_edge(diagram, starting_region_label, starting_region_cutted_label, edge_to_slide_index, last_edge_index, edges_to_go_through[-1][::-1], new_red_edge_enter_starting_region, new_red_edge_enter_starting_region_cutted)			


			# We check if there was a basepoint in starting_region that was not modified by the move
			# but stayied in starting_region_cutted and hence is to modify in the basepoint dictionary
			check_if_red_edge_on_starting_region_cutted_handleslide(diagram, starting_region_label, starting_region_cutted, starting_region_cutted_label)


			# We check if there was a basepoint in starting_region that was not modified by the move
			# but now is in neighbour_region and hence is to modify in the basepoint dictionary
			check_if_red_edge_on_starting_region_cutted_handleslide(diagram, starting_region_label, new_neighbour_region, neighbour_region.label)



	# Before iterating the move on the middle regions, there is a check to do:
	# we need to check if we are going to cut again through the first and the last red edge;
	# in such case we need to substitute the old edges with the newly created in the list of 
	# edges to go through (remark that one edge can be passed only two times at maximum)


	# We check the first edge in the opposite orientation, i.e. if it is going to be 
	# an entering edge for starting region, starting_region_cutted or neighbour_region
	# (as entering edge, it will be saved under "index_temp")
	if edges_to_go_through[0][::-1] in edges_to_go_through[1:-1]:

		# We recover the edge of the starting edge cutted in the other way
		index_temp = edges_to_go_through.index(edges_to_go_through[0][::-1])

		# We substitute it with the new edge that we created
		internal_edges_dictionary[index_temp]['entering_edge'] = [number_intersection_points + 1, edges_to_go_through[0][1]]


	# We check the last edge in the opposite orientation, i.e. if it is going to be 
	# an exiting edge for starting region, starting_region_cutted or neighbour_region
	# (as exiting edge, it will be saved under "index_temp - 1")
	if edges_to_go_through[-1][::-1] in edges_to_go_through[1:-1]:

		# We recover the edge of the starting edge cutted in the other way
		index_temp = edges_to_go_through.index(edges_to_go_through[-1][::-1])

		# We substitute it with the new edge that we created
		internal_edges_dictionary[index_temp - 1]['exiting_edge'] = [edges_to_go_through[-1][1], number_intersection_points + len(edges_to_go_through)]





	# We need to modify one last thing before iterating: now we have splitted
	# the starting region in two and possibly some red edges went inside neighbour region;
	# therefore now we need to modify the lists of regions to cut through, substituting 
	# the original region when needed

	# We start by understanding when we go inside the starting region
	indicies_visits_starting_region = [index for index in range(len(regions_to_go_through) - 1) if regions_to_go_through[index] == starting_region_label]

	# We take the red edges of both regions
	red_edges_starting_region = list(map(list, zip(starting_region, starting_region[1:]+ [starting_region[0]])))[::2]
	red_edges_starting_region_cutted = list(map(list, zip(starting_region_cutted, starting_region_cutted[1:]+ [starting_region_cutted[0]])))[::2]
	red_edges_new_neighbour_region = list(map(list, zip(new_neighbour_region, new_neighbour_region[1:]+ [new_neighbour_region[0]])))[::2]

	# And then we check the entering edge of the region at all the indicies
	for index in indicies_visits_starting_region:

		entering_edge = internal_edges_dictionary[index]['entering_edge']
		
		# We check if we are entering in starting_region, in starting_region_cutted
		# or in neighbour_region
		if entering_edge in red_edges_starting_region:
			
			# In this case, we don't need to do anything
			pass
			
		elif entering_edge in red_edges_starting_region_cutted:

			# We need to change the label of the region that we are in
			regions_to_go_through[index] = starting_region_cutted_label

		elif entering_edge in red_edges_new_neighbour_region:

			# We need to change the label of the region that we are in
			regions_to_go_through[index] = neighbour_region.label

		else:

			# Sanity check, this shouldn't happen
			sys.exit('Problem: doing a generalized handleslide and ripartitioning the edges between starting_region and starting_region_cutted something is wrong')


	

	
	# We can now iterate the procedure on the middle regions

	# We keep track of the regions that we modified already (we are 
	# not going to go in order as usual, but we do all the modification
	# on the same region at once)
	regions_to_go_through_set = set(regions_to_go_through)

	while regions_to_go_through_set:
		
		# We take one region that we didn't fix yet
		middle_region_label = regions_to_go_through_set.pop()
		middle_region = regions_input[middle_region_label - 1]

		# We understand when we go inside middle region
		indicies_visits_middle_region = [index for index in range(len(regions_to_go_through) - 1) if regions_to_go_through[index] == middle_region_label]

	

		# We iterate on the number of visits of the region

		for index in indicies_visits_middle_region:

			# We find the index of the red edge that we use for exiting from the region
			edge_exiting_middle_region = internal_edges_dictionary[index]['exiting_edge']
			edge_exiting_middle_region_index = get_index_of_edge(middle_region, edge_exiting_middle_region)
			
			
			# Then we need the index of the red edge that we use to enter in the region
			edge_entering_middle_region = internal_edges_dictionary[index]['entering_edge']
			edge_entering_middle_region_index = get_index_of_edge(middle_region, edge_entering_middle_region)
			
			
			# We can now generate the new region and modify the last middle region
			# We need to be careful in the case of a bigon: if the entering adge is the same of 
			# the exiting edge, we need to do a variation on the modification
			if edge_entering_middle_region_index == edge_exiting_middle_region_index:

				# We are modifying a bigon
				middle_region_cutted = [number_intersection_points + 1 + index] + middle_region[::-1] + [number_intersection_points + 1 + (index + 1)]
				middle_region = [number_intersection_points + 1 + (index + 1), number_intersection_points + 1 + index]
				
				# We define the new edges to eventually substitute in the basepoint dictionary
				new_entering_edge = [number_intersection_points + 1 + (index + 1), number_intersection_points + 1 + index]
				new_exiting_edge = [number_intersection_points + 1 + (index + 1), number_intersection_points + 1 + index]

			else:

				# We are not modifying a bigon
				if edge_entering_middle_region_index < edge_exiting_middle_region_index:
					middle_region_cutted = [number_intersection_points + 1 + index] + middle_region[edge_entering_middle_region_index + 1:edge_exiting_middle_region_index + 1] + [number_intersection_points + 1 + (index + 1)]
					middle_region = [number_intersection_points + 1 + (index + 1)] + middle_region[edge_exiting_middle_region_index + 1:] + middle_region[0:edge_entering_middle_region_index + 1] + [number_intersection_points + 1 + index]
				else:
					middle_region_cutted = [number_intersection_points + 1 + index] + middle_region[edge_entering_middle_region_index + 1:] + middle_region[0:edge_exiting_middle_region_index + 1] + [number_intersection_points + 1 + (index + 1)]
					middle_region = [number_intersection_points + 1 + (index + 1)] + middle_region[edge_exiting_middle_region_index + 1:edge_entering_middle_region_index + 1] + [number_intersection_points + 1 + index]
			
				
				# We define the new edges to eventually substitute in the basepoint dictionary
				new_entering_edge = [edge_entering_middle_region[0], number_intersection_points + 1 + index]
				new_exiting_edge = [number_intersection_points + 1 + (index + 1), edge_exiting_middle_region[1]]
		


			



			# For diagrams of 4-ended tangles:
			# We check if middle_region is a region with basepoint in the case in which we have
			# closed the surface
			if diagram.is_tangle_diagram:
				
				check_and_fix_basepoint_generalized_handleslide(diagram, regions_to_go_through[index], edge_entering_middle_region, edge_exiting_middle_region, new_entering_edge, new_exiting_edge)




			# We need to check if we modified a red edge that we'll use for later operation
			# Remark that we compare them in the opposite order (we can't come in ot go out
			# twice from the same edge)
			for future_index in indicies_visits_middle_region[indicies_visits_middle_region.index(index) + 1: ]:

				# We check the entering edge
				future_entering = internal_edges_dictionary[future_index]['entering_edge']
				if future_entering == edge_exiting_middle_region:

					# If it is the same, we need to modify this edge
					internal_edges_dictionary[future_index]['entering_edge'] = [number_intersection_points + 1 + (index + 1), edge_exiting_middle_region[1]]
				

				# We check the exiting edge
				future_exiting = internal_edges_dictionary[future_index]['exiting_edge']
				if future_exiting == edge_entering_middle_region:

					# If it is the same, we need to modify this edge
					internal_edges_dictionary[future_index]['exiting_edge'] = [edge_entering_middle_region[0], number_intersection_points + 1 + index]
			





			# We save all the results in regions_input
			regions_input[regions_to_go_through[index] -1] = middle_region
			regions_input.append(middle_region_cutted)



		
		
		




	# We can now update our diagram
	# We modify the attributes
	diagram.NEW_regions_input = regions_input
	diagram.NEW_number_intersection_points = number_intersection_points + len(edges_to_go_through)

	# We update the diagram
	diagram.update_diagram()