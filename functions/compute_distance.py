def compute_distance(diagram):
    regions = diagram.regions 
    multiplicity_zero_regions = diagram.multiplicity_zero_regions
    
    # We assign distance 0 to the regions with basepoint
    # To do so, we must distinguish between the case of a 
    # 4-ended tangle diagram and any other possibility
    if diagram.is_tangle_diagram:
        for couple in diagram.basepoints_p_or_q:
            regions[couple[0]].distance = 0
            regions[couple[0]].p_or_q = ((1 - couple[1]) * 'p') + (couple[1] * 'q')
    else:
        for index in multiplicity_zero_regions:
            regions[index].distance = 0

    keys_temp = list(regions.keys())

    while keys_temp != []:

        # We consider the first index from the list and we temporarely remove it from the list
        index_temp = keys_temp[0] 
        keys_temp = keys_temp[1:] 

        # We now check if the taken region has already  the distance assigned, in such case
        # we assign the distance to all its blue neighbours 
        # To do so, we must distinguish between the case of a 
        # 4-ended tangle diagram and any other possibility
        if diagram.is_tangle_diagram:
            if regions[index_temp].distance >= 0:
                for neighbour in regions[index_temp].blue_neighbours:
                    if neighbour[0].distance == -1:

                        neighbour[0].distance = regions[index_temp].distance + 1

                        # We also assign the p_or_q value to the region
                        neighbour[0].p_or_q = regions[index_temp].p_or_q
                    
            # If the region that we tried to use doesn't have the distance yet, 
            # we put its index at the end of the list
            else:  
                keys_temp.append(index_temp)
                
        else:
            if regions[index_temp].distance >= 0:
                for neighbour in regions[index_temp].blue_neighbours:
                    if neighbour[0].distance == -1:
                        
                        neighbour[0].distance = regions[index_temp].distance + 1
                        

            # If the region that we tried to use doesn't have the distance yet, 
            # we put its index at the end of the list
            else:  
                keys_temp.append(index_temp)