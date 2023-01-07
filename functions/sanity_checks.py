import sys


# Sanity check: there isn't any circle with only two points on it

def check_no_circle_one_or_two_points(red_circles_input, blue_circles_input):
	for index in range(len(red_circles_input)):
		circle = red_circles_input[index]
		if len(circle) == 2:
			s = 'Error in input:\n	check red circle number %d, we have only two intersection points on it.' %(index+1) 
			s = s+ '\n	Do a finger move in order to have at least three intersection points on it.'
			sys.exit(s)
		if len(circle) == 1:
			s = 'Error in input:\n	check red circle number %d, we have only one intersection point on it.' %(index+1) 
			s = s+ '\n	Do a finger move in order to have at least three intersection points on it.'
			sys.exit(s)

	for index in range(len(blue_circles_input)):
		circle = blue_circles_input[index]
		if len(circle) == 2:
			s = 'Error in input:\n	check blue circle number %d, we have only two intersection points on it.' %(index+1) 
			s = s+ '\n	Do a finger move in order to have at least three intersection points on it.'
			sys.exit(s)

		if len(circle) == 1:
			s = 'Error in input:\n	check blue circle number %d, we have only one  intersection point on it.' %(index+1) 
			s = s+ '\n	Do a finger move in order to have at least three intersection points on it.'
			sys.exit(s)





# Sanity check: all the blue and red edges are counted twice (in both directions)

def check_all_edges_twice(diagram):

	# Variables needed
	regions = diagram.regions
	blue_circles = diagram.blue_circles
	red_circles = diagram.red_circles
	red_arcs = diagram.red_arcs

	# Setup for the check
	blue_edges_sanity = []
	red_edges_sanity = []
	blue_edges_regions_sanity = []
	red_edges_regions_sanity = []
	error_flag = False


	# We create the list of edges that appear in the input od the circles and the arcs
	for arc in red_arcs:
		edges_in_arc = [[arc[i], arc[i+1]] for i in range(len(arc)-1)]
		red_edges_sanity = red_edges_sanity + edges_in_arc

	for circle in red_circles:
		edges_in_circle = [[circle[i], circle[i+1]] for i in range(len(circle)-1)] + [[circle[-1], circle[0]]]
		red_edges_sanity = red_edges_sanity + edges_in_circle

	for circle in blue_circles:
		edges_in_circle = [[circle[i], circle[i+1]] for i in range(len(circle)-1)] + [[circle[-1], circle[0]]]
		blue_edges_sanity = blue_edges_sanity + edges_in_circle
		
	
	# We create the lists of edges that appear in the regions
	for index in regions:
		reg = regions[index]
		blue_edges_regions_sanity = blue_edges_regions_sanity + reg.blue_edges
		red_edges_regions_sanity = red_edges_regions_sanity + reg.red_edges


	# Now we check that all the edges that are in the list of circles and arcs are
	# indeed edges of the regions (and here are counted twice in opposite directions).


	# Check on red edges
	while (red_edges_sanity) and (not error_flag):
		edge_to_check = red_edges_sanity.pop(0)
		if (edge_to_check in red_edges_regions_sanity) and (edge_to_check[::-1] in red_edges_regions_sanity):
					red_edges_regions_sanity.remove(edge_to_check)
					red_edges_regions_sanity.remove(edge_to_check[::-1])
		else:
			error_flag = True

	if error_flag:
		sys.exit(f"Error in the input: we can't find the inverse of the red edge {edge_to_check}. \nCheck the RED edges (or the orientation of the regions)")


	# Check on blue edges
	while (blue_edges_sanity) and (not error_flag):
		edge_to_check = blue_edges_sanity.pop(0)
		if (edge_to_check in blue_edges_regions_sanity) and (edge_to_check[::-1] in blue_edges_regions_sanity):
					blue_edges_regions_sanity.remove(edge_to_check)
					blue_edges_regions_sanity.remove(edge_to_check[::-1])
		else:
			error_flag = True

	if error_flag:
		sys.exit(f"Error in the input: we can't find the inverse of the blue edge {edge_to_check}. \nCheck the BLUE edges (or the orientation of the regions)")




'''   Failed attempt of a sanity check
# Check on red edges
for i in regions:
	counter = 0
	for edge in red_edges_sanity[i]:
		for j in regions:
			if edge[::-1] in red_edges_sanity[j]:
				counter = counter + 1
	
	if counter != len(red_edges_sanity[i]):
		error_flag = True
		print('RED Error in the input, check the edges (or the orientation of the regions)') #[%d, %d]' %(edge[0], edge[1]))

# Check on blue edges
for i in regions:
	counter = 0
	for edge in blue_edges_sanity[i]:
		for j in regions:
			if edge[::-1] in blue_edges_sanity[j]:
				counter = counter + 1
				break
	
	if counter != len(blue_edges_sanity[i]):
		error_flag = True
		print('BLUE Error in the input, check the edges (or the orientation of the regions)') #[%d, %d]' %(edge[0], edge[1]))
	
'''



def check_on_the_correctness_of_basepoints_dictionary(diagram, already_notified):
	
	if diagram.is_tangle_diagram:
		for key in diagram.basepoint_regions_and_red_edges.keys():
			if type(key)==tuple:
				if (key[::-1] not in diagram.basepoint_regions_and_red_edges.keys()) and (not already_notified):
					
					already_notified = True

					input(f"Problem with the red edges and basepoints: they don't coincide on both sides.\nWe can't find the inverse of {key}. \nPress Enter to see the last modification done to the diagram")
						
					'''
					s = ""
					s = s + "\n	Regions of the last diagram that we modified: "

					s = s + "\n		Type of move: %s" %H_diagram.last_diagram_regions_modified[-1]
					s = s + "\n		Starting region: Region %d" %H_diagram.last_diagram_regions_modified[0]
					s = s + "\n		Edge modified: %s" %str(H_diagram.last_diagram_regions_modified[1])
					s = s + "\n		Ending region: Region %d" %H_diagram.last_diagram_regions_modified[-3]
					s = s + "\n		Neighbor region: Region %d" %H_diagram.last_diagram_regions_modified[-2]
					s = s + "\n		Middle regions:"

					if H_diagram.last_diagram_regions_modified[2] == []:
						s = s + " None"
					else:
						for label in H_diagram.last_diagram_regions_modified[2]:
							s = s + "\n			Region %d" %label
							
					s = s + "\n		Edges crossed:"
					for edge in H_diagram.last_diagram_regions_modified[3]:
						s = s + "\n			%s" %str(edge)

						s = s + "\n"
					'''

					print('Type of move: %s' %diagram.last_diagram_regions_modified[-1])
					input("If you want to proceed with the algorithm, press Enter")