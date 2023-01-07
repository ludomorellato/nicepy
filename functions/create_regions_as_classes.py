from classes.region_class import Region

def regions_as_classes(regions_input, number_border_points):
    regions = dict()
    for i in range(len(regions_input)):
        region_temp = regions_input[i]
        
        red_edges = []
        blue_edges = []
        border_edges = []

        # List of border edges
        for j in range(len(region_temp)-1):
            if (region_temp[j] <= number_border_points) and (region_temp[j+1] <= number_border_points):
                border_edges.append([region_temp[j], region_temp[j+1]])

        # List of red edges
        for j in range(0,len(region_temp),2):
            if (region_temp[j] > number_border_points) or (region_temp[j+1] > number_border_points):
                red_edges.append([region_temp[j], region_temp[j+1]])

        # List of blue edges
        for j in range(1, len(region_temp)-1, 2):
            if (region_temp[j] > number_border_points) or (region_temp[j+1] > number_border_points):
                blue_edges.append([region_temp[j], region_temp[j+1]])

        # We fix the last edge
        if (region_temp[-1] > number_border_points) or (region_temp[0] > number_border_points):
            blue_edges.append([region_temp[-1], region_temp[0]])
        else:
            border_edges.append([region_temp[-1], region_temp[0]])
            

        regions[i+1] = Region(i+1, int(len(region_temp)/2), red_edges, blue_edges, border_edges, regions_input[i])
    
    return regions