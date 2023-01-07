# In the case of a diagram for a 4-ended tangle, we want to eliminate the borders and 
# obtain an alpha circle instead of four alpha arcs. We also generate new basepoints
# that count more than 0 in the sense of the multiplicity where we close the borders
# (in the case in which we don't have a mulitplicity zero basepoint)

from functions.get_index_of_edge import get_index_of_edge
from classes.Heegaard_Diagram_class import Heegaard_diagram

def close_4_ended_tangle_diagram(diagram):
	
	number_border_points = diagram.number_border_points
	number_intersection_points = diagram.number_intersection_points
	regions_input = diagram.regions_input
	multiplicity_zero_regions = diagram.multiplicity_zero_regions

	# We want to place the basepoints in the right regions with a red edge linked to them;
	# we construct a dictionary:the keys are the regions with a basepoint and the values are
	# lists of the associated red_edges
	basepoint_regions_and_red_edges = dict()

	# We also want to remember the number of border points and the right place in which they where
	# To do so, we'll also save the border component under the key "red_edge"



	for label in diagram.border_regions:

		# We take a border region
		region_input = regions_input[label - 1]

		if len(diagram.regions[label].border_edges) == 1:
			
			# This is the case in which the region that we are considering has only one border component
			border_edge = diagram.regions[label].border_edges[0]

			index_border_point = get_index_of_edge(region_input, border_edge)

			 # We distinguish between the case in which the border edge is the last edge of the input or not
			if index_border_point == len(region_input) - 1:
				
				# In this case it is the last edge of the input, we cut it out
				new_region_input = [region_input[-2]] + region_input[1:-2]
				regions_input[label - 1] = new_region_input
				red_edge_scaled = [x - number_border_points for x in new_region_input[0:2]]

				# We save both the red edge under the region label and the border edge under the red edge data
				basepoint_regions_and_red_edges[label] = [red_edge_scaled]
				basepoint_regions_and_red_edges[tuple(red_edge_scaled)] = border_edge

			else:

				# In this case is not the last edge of the input
				new_region_input = region_input[0 : index_border_point] + region_input[index_border_point + 2 : ]
				regions_input[label - 1] = new_region_input
				red_edge_scaled = [x - number_border_points for x in new_region_input[index_border_point - 1 : index_border_point + 1]]
				
				# We save both the red edge under the region label and the border edge under the red edge data
				basepoint_regions_and_red_edges[label] = [red_edge_scaled]
				basepoint_regions_and_red_edges[tuple(red_edge_scaled)] = border_edge
		
		else:

			# We create an empty list under the key "label"
			basepoint_regions_and_red_edges[label] = []
			

			# Now we append the right red edges to the list
			for border_edge in diagram.regions[label].border_edges:

				index_border_point = get_index_of_edge(region_input, border_edge)

				if index_border_point == len(region_input) - 1:
					
					new_region_input = [region_input[-2]] + region_input[1:-2]
					regions_input[label - 1] = new_region_input
					red_edge_scaled = [x - number_border_points for x in new_region_input[0:2]]

					# We save both the red edge under the region label and the border edge under the red edge data
					basepoint_regions_and_red_edges[label].append(red_edge_scaled)
					basepoint_regions_and_red_edges[tuple(red_edge_scaled)] = border_edge

				else:
					new_region_input = region_input[0 : index_border_point] + region_input[index_border_point + 2 : ]
					regions_input[label - 1] = new_region_input
					red_edge_scaled = [x - number_border_points for x in new_region_input[index_border_point - 1 : index_border_point + 1]]
				
					# We save both the red edge under the region label and the border edge under the red edge data
					basepoint_regions_and_red_edges[label].append(red_edge_scaled)
					basepoint_regions_and_red_edges[tuple(red_edge_scaled)] = border_edge
		


	regions_input_scaled = [[x - number_border_points for x in region] for region in regions_input]
	

	# We set the new values to update the diagram

	diagram.NEW_regions_input = regions_input_scaled
	diagram.NEW_multiplicity_zero_regions = multiplicity_zero_regions
	diagram.NEW_number_intersection_points = number_intersection_points - number_border_points
	diagram.NEW_number_border_points = 0
	diagram.basepoint_regions_and_red_edges = basepoint_regions_and_red_edges

	# We update the diagram
	
	diagram.update_diagram()