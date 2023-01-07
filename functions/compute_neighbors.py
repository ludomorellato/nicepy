def compute_neighbors(diagram):
	for i in diagram.regions.keys():

        # We compute the red neighbors
		for edge in diagram.regions[i].red_edges:
			for j in diagram.regions.keys():
				if edge[::-1] in diagram.regions[j].red_edges:
					diagram.regions[i].add_neighbor([diagram.regions[j],edge], 'red')
					break
        
        # We compute the blue neighbors
		for edge in diagram.regions[i].blue_edges:
			for j in diagram.regions.keys():
				if edge[::-1] in diagram.regions[j].blue_edges:
					diagram.regions[i].add_neighbor([diagram.regions[j],edge], 'blue')
					break