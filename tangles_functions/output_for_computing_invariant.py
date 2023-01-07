# Function that creates as output the input for PQM.m Mathematica Software

import sys

from functions.get_index_of_edge import get_index_of_edge

from classes.Heegaard_Diagram_class import Heegaard_diagram



def output_for_computing_invariant(diagram, number_border_points, alpha_arcs_sites, alexander_grading):
	

	# If we are in this case, we want to do a few operations first on the diagram
	# To nicefy it, we started from a close diagram (or we closed it ourselves);
	# now we need to make a step back in this direction and to re-add the border components.
	# To do so, we use the knowledge of where the basepoints are placed after the 
	# nicefication process, we basically need to split the alpha circle with all the
	# basepoints (i.e. red edges) in the right spots.


	# We modify direclty what we'll need as input for the new bordered diagram 
	regions_input = diagram.regions_input
	number_intersection_points = diagram.number_intersection_points


	'''
	

	# We shift all the verticies of the diagram by adding number_border_points
	regions_input_scaled = [[x + number_border_points for x in region] for region in regions_input]

	# We add the old border components in the same spot using diagram.basepoint_regions_and_red_edges

	for key in diagram.basepoint_regions_and_red_edges.keys():
		if type(key) == tuple:
			pass
		elif type(key) == int:
			
			for edge in diagram.basepoint_regions_and_red_edges[key]:

				region_label = key
				red_edge = [x + number_border_points for x in edge]
				border_edge = diagram.basepoint_regions_and_red_edges[tuple(edge)]

				index_red_edge = get_index_of_edge(regions_input_scaled[key-1], red_edge)
				
				regions_input_scaled[key-1] = regions_input_scaled[key-1][ : index_red_edge + 1] + border_edge + regions_input_scaled[key-1][index_red_edge+1 : ]
	'''


 
	# We move the multiplicity zero regions to the end of the list of regions and we modify the basepoint dictionary consequentially

	multiplicity_zero_regions = []
	p_or_q = []
	basepoint_regions_and_red_edges = dict()

	# We extract the multiplicity zero regions from the regions input
	multiplicity_zero_regions_input_p_or_q = []
	old_labels = []

	for [label, basepoint] in diagram.basepoints_p_or_q:
		multiplicity_zero_regions_input_p_or_q.append([regions_input[label - 1].copy(), basepoint])
		old_labels.append(label)


	# Then, we eliminate them from the regions input and we append them in the last spots
	# We keep track of how many they are
	number_multiplicity_zero_regions = len(old_labels)

	while old_labels:

		# We remove them starting from the biggest index, so that we don't need to keep track of possible translations
		max_label = max(old_labels)

		# We remove max_label from the list of old labels
		old_labels.remove(max_label)

		region_to_move = regions_input[max_label - 1]
		
		# We delete it
		del regions_input[max_label - 1]

		# We append it
		regions_input.append(region_to_move)

	
	
	# Now we need to update the information in p_or_q
	for index in range(len(regions_input) - number_multiplicity_zero_regions, len(regions_input)):

		new_label = index + 1

		# We need to see if it is a p region or a q region
		region_temp = regions_input[index]

		# We find it back in multiplicity_zero_regions_input_p_or_q
		for [possible_same_region, basepoint] in multiplicity_zero_regions_input_p_or_q:

			if possible_same_region == region_temp:

				# If it is the same, we use this basepoint 
				p_or_q.append([new_label, basepoint])
				multiplicity_zero_regions.append(new_label)
				basepoint_regions_and_red_edges[new_label] = [0]
				
				# We remove this region from multiplicity_zero_regions_input_p_or_q
				multiplicity_zero_regions_input_p_or_q.remove([possible_same_region, basepoint])

				# And we break the cycle
				break

	'''
	for [label, basepoint] in diagram.basepoints_p_or_q:

		region_to_move = regions_input[label - 1 - counter]
		del regions_input[label - 1 - counter]
		regions_input.append(region_to_move)
		
		p_or_q.append([new_label, basepoint])
		multiplicity_zero_regions.append(new_label)
		basepoint_regions_and_red_edges[new_label] = [0]

		new_label = new_label + 1
		counter = counter + 1
	'''

	# We add to basepoint_regions_and_red_edges the other basepoint regions with the right new label
	for key in diagram.basepoint_regions_and_red_edges.keys():
		if type(key) == int:

			# We don't consider the multiplicty zero regions
			if key in diagram.multiplicity_zero_regions:
				
				# We save the border component that we have eliminated in the beginning and the new red edge
				basepoint_regions_and_red_edges[tuple(diagram.basepoint_regions_and_red_edges[key][0])] = diagram.basepoint_regions_and_red_edges[tuple(diagram.basepoint_regions_and_red_edges[key][0])]

			else:

				# We need to understand how many regions were before this one
				labels_before_key = [label for label in diagram.multiplicity_zero_regions if label < key]

				# Now we save the basepoint region label with the right new label
				basepoint_regions_and_red_edges[key - len(labels_before_key)] = [0]

				# And we save the border component that we have eliminated in the beginning and the new red edge
				basepoint_regions_and_red_edges[tuple(diagram.basepoint_regions_and_red_edges[key][0])] = diagram.basepoint_regions_and_red_edges[tuple(diagram.basepoint_regions_and_red_edges[key][0])]


	# We create the basepoint_dictionary
	basepoints_dictionary = dict()

	basepoints_dictionary['multiplicity_zero_regions'] = multiplicity_zero_regions
	basepoints_dictionary['basepoint_regions_and_red_edges'] = basepoint_regions_and_red_edges
	basepoints_dictionary['p_or_q'] = p_or_q

	H_diagram_for_output = Heegaard_diagram(number_intersection_points, 0, regions_input, basepoints_dictionary, False)

	





	# We have now a close nice diagram with the regions in the right order
	
	# As first thing, we break the basepoint_regions_and_red_edges dictionary in two distinc dictionaries
	# that are more easy to handle

	basepoints_regions_dictionary = dict()
	red_edges_and_border_components_dictionary = dict()

	for key in H_diagram_for_output.basepoint_regions_and_red_edges:

		if type(key) == int:
			basepoints_regions_dictionary[key] = []
		
		elif type(key) == tuple:
			red_edges_and_border_components_dictionary[key] = H_diagram_for_output.basepoint_regions_and_red_edges[key]













	# MANUALLY CREATING THE ALPHA ARCS

	# We need to manually open the alpha circle in the four alpha arcs before porceeding with the
	# output construction

	alpha_circles = H_diagram_for_output.red_circles

	for key in red_edges_and_border_components_dictionary:
		red_edge = list(key)
		break
	
	for index in range(len(alpha_circles)):
		
		# We create all the red edge of the circle
		circle_zipped = list(map(list, zip(alpha_circles[index], alpha_circles[index][1:]+ [alpha_circles[index][0]])))
	
		# We search for our red edge
		if (red_edge in circle_zipped) or (red_edge[::-1] in circle_zipped):

			# We are looking at the right circle, therefore we save it and we break the cycle
			# (we don't eliminate the circle from the list of circles since the program wants it there)
			circle_to_open = alpha_circles[index]
			break
		
		else:
			pass 

	

	# We must now understand where we need to break open the circle
	
	spot_to_open = []
	
	# We look through the keys of red_edges_and_border_components_dictionary, which are exaclty 
	# the red edges on which we'll open the circle
	for key in red_edges_and_border_components_dictionary:

		red_edge = list(key)

		# We could have that red_edge is in circle_zipped or that red_edge[::-1] is in circle_zipped, 
		# therefore we need to do this check
		if red_edge in circle_zipped: 
				
			spot_to_open.append(red_edge)

	
	# We create the four arcs
	indicies_where_to_open = []

	for edge in spot_to_open:
		indicies_where_to_open.append(get_index_of_edge(circle_to_open, edge))

	indicies_where_to_open.sort()
	indicies_where_to_open = [-1] + indicies_where_to_open + [len(circle_to_open) - 1]

	arcs_not_in_order = []
	couple_of_indicies = list(zip(indicies_where_to_open[:-1], indicies_where_to_open[1:]))

	for (first_index, second_index) in couple_of_indicies:
		arcs_not_in_order.append(circle_to_open[first_index + 1: second_index + 1])


	# We glue the first and the last piece (if they are not trivial) as they are a unique arc
	# Then we eliminate the arcs in surplus

	if (len(arcs_not_in_order) == 5) and (arcs_not_in_order[0]) and (arcs_not_in_order[4]):
		
		arcs_not_in_order[0] = arcs_not_in_order[4] + arcs_not_in_order[0]
		arcs_not_in_order = arcs_not_in_order[:-1]

	elif  (len(arcs_not_in_order) == 5) and (arcs_not_in_order[0]):
		arcs_not_in_order = arcs_not_in_order[:-1]

	elif  (len(arcs_not_in_order) == 5) and (arcs_not_in_order[-1]):
		arcs_not_in_order = arcs_not_in_order[1:]

	else:
		pass


	
	# We now need to understand where the basepoint of alpha_arcs_sites should be in the closed diagram

	alpha_arcs_sites_closed_diagram = []

	for border_point in alpha_arcs_sites:

		# We look thorugh the keys of red_edges_and_border_components_dictionary, which are the red_edges that we 
		# we want to substitute the alpha_arcs_site data with
		for key in red_edges_and_border_components_dictionary.keys():
			
			# We exclude the keys in the wrong order (is not a problem thaat they are in the wrong order, 
			# but otherwise we'll count them twice)
			if list(key) in spot_to_open:

				# We check if the border point is the value under this red edge
				if border_point in red_edges_and_border_components_dictionary[key]:

					# If so, we understand if it is the firt or the second element of the 
					# border edge; we only need then to save the correspondant element of the
					# red edge (as the red edge is "around" of the border edge)
					if border_point == red_edges_and_border_components_dictionary[key][0]:

						alpha_arcs_sites_closed_diagram.append(key[0])
					
					else:
						
						alpha_arcs_sites_closed_diagram.append(key[1])


	# We create a list with the alpha circles saved in the right order, corresponding to
	# site "a", site "b", site "c" and site "d".

	alpha_arcs_ordered = []

	# We take one intersection point in alpha_arcs_sites_closed_diagram
	for intersection_point in alpha_arcs_sites_closed_diagram:

		# We look thorugh all the arcs to find the one that cointains it, then we append 
		# such arc to the ordered list of arcs and we break this second for
		for arc in arcs_not_in_order:
			
			if intersection_point in arc:
				
				alpha_arcs_ordered.append(arc)
				break

	











	# MANUALLY UNDERSTANDING THE ALEXANDER GRADINGS

	# We want now link the right red edge and border edge to the right basepoint region
	# in order to be able to use the Alexander gradings input that we have
	
	# First we generate all the red edges of the basepoint regions; we iterate on the keys of
	#  basepoints_regions_dicionary, which are exaclty the labels of the basepoint regions
	for key in basepoints_regions_dictionary:
			
		# We generate all the red edges of this region
		region_temp = H_diagram_for_output.regions[key].input
		region_zipped = list(map(list, zip(region_temp, region_temp[1:] + [region_temp[0]])))
		region_zipped_red_edges = region_zipped[::2]
	

		# Now we find for every regions which is the right red edge where we have the basepoint
		for red_edge_tuple in red_edges_and_border_components_dictionary.keys():

			red_edge = list(red_edge_tuple)

			if red_edge in region_zipped_red_edges:

				basepoints_regions_dictionary[key].append(red_edge)
				basepoints_regions_dictionary[key].append(red_edges_and_border_components_dictionary[tuple(red_edge)])




	# We save the alexander gradings in a new dictionary, called alexander_grading_dictionary
	# We put as keys the labels of the basepoint regions and as values empty lists
	alexander_grading_dictionary = basepoints_regions_dictionary.copy()
	for key in alexander_grading_dictionary.keys():
		alexander_grading_dictionary[key] = []

	# We create a list of the gradings
	gradings = [[1,0], [-1,0], [0,1], [0,-1]]

	# We take a key of basepoint_regions_dictionary, which is a label of a basepoint region
	for label in basepoints_regions_dictionary.keys():

		first_border_point = basepoints_regions_dictionary[label][1][0]
		second_border_point = basepoints_regions_dictionary[label][1][1]

		# We understand the index of the Alexander grading by watching which of the border component is in this region
		for index in range(len(alexander_grading)):
			if (alexander_grading[index] == first_border_point) or (alexander_grading[index] == second_border_point):
				break 
		
		alexander_grading_dictionary[label].append(gradings[index])


	# We now sum all the gradings under one label
	for label in alexander_grading_dictionary.keys():
		
		sum_gradings = [0,0]
		
		for grade in alexander_grading_dictionary[label]:
			sum_gradings[0] = sum_gradings[0] + grade[0]
			sum_gradings[1] = sum_gradings[1] + grade[1]

		# We put the final grading as the only value of label in alexander_grading_dictionary
		alexander_grading_dictionary[label] = tuple(sum_gradings)
	































	# GOOD REGIONS

	# We need a matrix with five columns with the good regions. The first column 
	# gives the label of the region, then we have one intersection point per column
	# (in the case of bigons we fill out the voids with "\[Placeholder]") 
	# The matrix is written as {{1,2,3,4,5},{6,7,8,9,10}, ...}
	# The program require the region to be writte clock-wise and starting from a red 
	# edge, hence we need to play a bit with our notation
	
	good_regions_output_string = "regionsInput = ( {"
	good_regions_labels = set(range(1, H_diagram_for_output.number_of_regions + 1)) - set(H_diagram_for_output.multiplicity_zero_regions)
	
	for label in good_regions_labels:

		good_regions_output_string = good_regions_output_string + "{" + str(label) + ","
		if H_diagram_for_output.regions[label].number_edges == 4:

			for intersection in H_diagram_for_output.regions[label].input[::-1]:
				good_regions_output_string = good_regions_output_string + str(intersection)  + ","

		else:

			for intersection in H_diagram_for_output.regions[label].input[::-1]:
				good_regions_output_string = good_regions_output_string + str(intersection)  + ","

			good_regions_output_string = good_regions_output_string + "\[Placeholder],\[Placeholder],"

		good_regions_output_string = good_regions_output_string[:-1] + "},"

	
	good_regions_output_string = good_regions_output_string[:-1] + "} ); \n \n"


	


	




	# ALPHA CIRCLES

	# We need a matrix with two columns and as many rows as many alpha circles. The first
	# entry is the label of the circle, the second is a list (not in a specific order)
	# of the intersection points on such alpha circle

	alpha_circles_output_string = "alphasInput = ( {"

	for label in range(len(alpha_circles)):

		alpha_circles_output_string = alpha_circles_output_string + "{" + str(label + 1) + ",{"
		alpha_circles_output_string = alpha_circles_output_string + str(alpha_circles[label])[1:-1] + "}" + "},"


	alpha_circles_output_string = alpha_circles_output_string[:-1] + "} ); \n \n"










	# BETA CIRCLES

	# We need a matrix with two columns and as many rows as many beta circles. The first
	# entry is the label of the circle, the second is a list (not in a specific order)
	# of the intersection points on such beta circle

	beta_circles_output_string = "betasInput = ( {"

	for label in range(len(H_diagram_for_output.blue_circles)):

		beta_circles_output_string = beta_circles_output_string + "{" + str(label + 1) + ", {"
		beta_circles_output_string = beta_circles_output_string + str(H_diagram_for_output.blue_circles[label])[1:-1] + "}" + "},"


	beta_circles_output_string = beta_circles_output_string[:-1] + "} ); \n \n"











	# CANCELLATION SORT LIST INPUT

	# Empty list for now, maybe we can fix it in the future
	cancellation_sort_output_string = 'cancellationSortListInput = ( { } ); \n \n' 










	# ALPHA ARCS

	# We need a matrix with two columns and four rows. The first is "a", "b", "c" or "d",
	# which are the labels of the four sites of the tangle; the second entry is a list
	# of the intersection points on such alpha arc.
	


	if len(alpha_arcs_ordered) != 4:
		sys.exit("Error: we are not dealing with a four endend tangle, we can't give the output for this other program")

	# We can construct the output
	alpha_arcs_output_string = "alphaArcs = ( {"

	for label in [('"a"',0), ('"b"', 1), ('"c"', 2), ('"d"',3)]:

		alpha_arcs_output_string = alpha_arcs_output_string + "{" + label[0] + ",{"
		alpha_arcs_output_string = alpha_arcs_output_string + str(alpha_arcs_ordered[label[1]])[1:-1] + "}" + "},"


	alpha_arcs_output_string = alpha_arcs_output_string[:-1] + "} ); \n \n"









	# BASEPOINT REGIONS

	# We need a matrix with four columns and as many rows as the regions with basepoints
	# (that are not multiplicity zero regions). 
	# The first entry is the label of the region.
	# The second entry is the type of basepoint that it has ("p" or "q"), in the very special
	# case that there are multiple basepoints in this region, we take a suitable power of p or q.
	# The third column corresponds to the Alexander grading.
	# The fourth column should be −2 (−4) for each basepoint of an open (closed) strand it contains.


	# We copy alexander_grading_dictionary and we remove the keys and values about the multiplicity
	# zero regions 
	basepoint_regions_ouput_dict = alexander_grading_dictionary.copy()

	for label in H_diagram_for_output.multiplicity_zero_regions:
		del basepoint_regions_ouput_dict[label]

	# We can start to contruct the string about the basepoint regions

	basepoint_regions_output_string = "basepointRegions = ( {"

	for label in basepoint_regions_ouput_dict.keys():

		basepoint_regions_output_string = basepoint_regions_output_string + "{" + str(label) + ", "
		basepoint_regions_output_string = basepoint_regions_output_string + H_diagram_for_output.regions[label].p_or_q + ","
		
		# We print the Alexander grading, which was already summed when we created alexander_grading_dictionary
		grade_1 = basepoint_regions_ouput_dict[label][0]
		grade_2 = basepoint_regions_ouput_dict[label][1]

		basepoint_regions_output_string = basepoint_regions_output_string + "{" + str(grade_1) + "," + str(grade_2) + "},"

		
		basepoint_regions_output_string = basepoint_regions_output_string + "-2},"

	
	basepoint_regions_output_string = basepoint_regions_output_string[:-1] + "} ); \n \n"












	# MULITPLICITY ZERO REGIONS

	# We need a matrix with four columns and as many rows as the mulitplicity zero regions.
	# The entries of the first column are indices of regions whose multiplicity in each domain is 0. 
	# The second entry is a list of oriented elementary β-segments (i.e. pairs of intersection points) 
	# along the boundary of the domain. The orientation conventions is clock-wise.
	# The third column corresponds to the Alexander grading; entries are lists of length equal to 
	# the number of colours in the tangle, such that the i-th entry of the list corresponds to the i-th
	# colour. A basepoint of an open (closed) strand leaving/entering the 3-manifold should be recorded 
	# as +1/−1 (+2/−2) for the corresponding colour. 
	# The entries of the fourth column should be 4·(Euler measure of region) plus −2 (−4) for each
	# basepoint of an open (closed) strand it contains.


	multiplicity_zero_regions_output_string = "multiplicity0Regions = ( {"

	for label in H_diagram_for_output.multiplicity_zero_regions:

		multiplicity_zero_regions_output_string = multiplicity_zero_regions_output_string + "{" + str(label) + ","
				
		# We generate the blue edges of region
		region = H_diagram_for_output.regions[label].input[::-1]
		region_zipped = list(map(list, zip(region, region[1:]+ [region[0]])))
		region_zipped_blue_edges = region_zipped[1::2]

		multiplicity_zero_regions_output_string = multiplicity_zero_regions_output_string + "{"

		for edge in region_zipped_blue_edges:

			multiplicity_zero_regions_output_string = multiplicity_zero_regions_output_string + "{" + str(edge[0]) + "," + str(edge[1]) + "},"

		
		multiplicity_zero_regions_output_string = multiplicity_zero_regions_output_string[:-1] + "},"


		# We print the Alexander grading, which was already summed when we created alexander_grading_dictionary
		grade_1 = alexander_grading_dictionary[label][0]
		grade_2 = alexander_grading_dictionary[label][1]
		multiplicity_zero_regions_output_string = multiplicity_zero_regions_output_string + "{" + str(grade_1) + "," + str(grade_2) + "},"
		


		# We compute the Euler characteristic of the region D, using the formula
		# 		e(D) = \chi(D) - 1/4·#convex_verticies + 1/4·#concave_verticies 
		# 			 = 2 - 1/4 #convex_verticies + 1/4 #concave_verticies 		(since regions are contractible)
		# 			 = 2 + 1/4·(- #convex_verticies + #concave_verticies)
		# 
		# To compute if a vertex is concave or convex, we just need to count how many times it appears the region's input,
		# if it appears one time is convex, if it appears three times it is concave
		
		region_set = set(region)

		# We count the appearance
		counted_appearance = [region.count(point) for point in region_set]

		# We sum the contributes
		sum_verticies_contributes = 8 # Since region are contractible, they have Euler characteristic 2, hence 4·2 = 8
		for contribute in counted_appearance:
			if contribute == 1:
				sum_verticies_contributes = sum_verticies_contributes - 1
			elif contribute == 3:
				sum_verticies_contributes = sum_verticies_contributes + 1
			else:
				pass
		
		# We compute the final fourth row
		# REMARK: for now it is only -2, I should distinguish between -2 and -4
		fourth_row = sum_verticies_contributes - 2

		multiplicity_zero_regions_output_string = multiplicity_zero_regions_output_string + str(fourth_row) + "},"

	
	multiplicity_zero_regions_output_string = multiplicity_zero_regions_output_string[:-1] + "} ); \n \n"














	# We compose the final output to print in one string
	output_string_to_print = good_regions_output_string + alpha_circles_output_string + beta_circles_output_string + cancellation_sort_output_string
	output_string_to_print = output_string_to_print + alpha_arcs_output_string + basepoint_regions_output_string + multiplicity_zero_regions_output_string


	# We compose the final output to save in the .txt document in one string
	output_string_to_save = "--------------------------------------------------\n"
	output_string_to_save = output_string_to_save + "This is the string to copy and paste as PQM.m Mathematica Package input:\n\n\n"
	output_string_to_save = output_string_to_save + good_regions_output_string + alpha_circles_output_string + beta_circles_output_string + cancellation_sort_output_string
	output_string_to_save = output_string_to_save + alpha_arcs_output_string + basepoint_regions_output_string + multiplicity_zero_regions_output_string
	output_string_to_save = output_string_to_save + "\n--------------------------------------------------\n"

	return output_string_to_print, output_string_to_save