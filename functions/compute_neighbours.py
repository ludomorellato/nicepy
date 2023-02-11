def compute_neighbours(diagram):
	for i in diagram.regions.keys():

        # We compute the red neighbours
		for edge in diagram.regions[i].red_edges:
			for j in diagram.regions.keys():
				if edge[::-1] in diagram.regions[j].red_edges:
					diagram.regions[i].add_neighbour([diagram.regions[j],edge], 'red')
					break
        
        # We compute the blue neighbours
		for edge in diagram.regions[i].blue_edges:
			for j in diagram.regions.keys():
				if edge[::-1] in diagram.regions[j].blue_edges:
					diagram.regions[i].add_neighbour([diagram.regions[j],edge], 'blue')
					break