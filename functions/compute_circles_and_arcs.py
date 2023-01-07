import numpy as np


def compute_red_arcs(regions_input, number_border_points, number_intersection_points):
    output_compute_red_arcs = dict()

    if number_border_points == 0:
        output_compute_red_arcs['red_arcs'] = []
        output_compute_red_arcs['intersection_points_remaining'] = list(range(1, number_intersection_points+1))
        return output_compute_red_arcs
    else:
        red_arcs = []

        # We make a list with all the border points on which we iterate and a list of 
        # intersection points to be sure that we wont go back on a same arc
        border_points_remaining = list(range(1, number_border_points + 1))
        intersection_points_remaining = list(range(1, number_intersection_points+1))

        # We now compute the arcs 
        while border_points_remaining != []:

            # We start an arc from a border point not already done, and we remove such 
            # point from both lists
            intersection_point_temp = border_points_remaining.pop(0)
            intersection_points_remaining.remove(intersection_point_temp)


            # We construct the arcs starting from the border point "intersection_point_temp"
            red_arcs.append([intersection_point_temp])

            # Exit flag for the following for cycle
            exit_flag_second_for_cycle = False

            # We find the second point and we append it to the arc
            for region in regions_input:
                if intersection_point_temp in region:
                    # we must consider the case in which the intersection point appears more than one 
                    # time in the region. We create an array with all the indicies of intersection_point
                    region_array = np.array(region)
                    searchval = intersection_point_temp
                    indicies_of_intersection_point_temp = np.where(region_array == searchval)[0]
                    
                    for index in indicies_of_intersection_point_temp:
                        if (index % 2 == 0) and (region[index + 1] in intersection_points_remaining):
                            
                            # We change intersection point and we append this new one to the arc
                            intersection_point_temp = region[index + 1]
                            red_arcs[-1].append(intersection_point_temp)

                            # Then we remove this intersection point from the list of remaining
                            # intersection points
                            intersection_points_remaining.remove(intersection_point_temp)

                            # We need to set a flag to exit from the first for cycle, otherwise
                            # the program is going to search also in the remaining regions if it 
                            # can continue the arc (and we want only to find the second point in this
                            # first block of code)
                            exit_flag_second_for_cycle = True
                            break

                    if exit_flag_second_for_cycle:

                        # If we have found the second point of the arc, we break the above for cycle
                        break
                    else:
                        pass
                    
            
            # We iterate until we reach the endpoint of the arc
            while intersection_point_temp > number_border_points:
                
                # Exit flag for the following for cycle
                exit_flag_second_for_cycle = False

                for region in regions_input:

                    if intersection_point_temp in region:

                        # we must consider the case in which the intersection point appears more than one 
                        # time in the region. We create an array with all the indicies of intersection_point
                        region_array = np.array(region)
                        searchval = intersection_point_temp
                        indicies_of_intersection_point_temp = np.where(region_array == searchval)[0]
                       
                        for index in indicies_of_intersection_point_temp:
                            if (index % 2 == 0) and (region[index + 1] in intersection_points_remaining):

                                # We change intersection point and we append this new one to the arc
                                intersection_point_temp = region[index + 1]
                                red_arcs[-1].append(intersection_point_temp)

                                # Then we remove this intersection point from the list of remaining
                                # intersection points
                                intersection_points_remaining.remove(intersection_point_temp)

                                # We need to set a flag to exit from the first for cycle, otherwise
                                # the program is going to search also in the remaining regions if it 
                                # can continue the arc (and we want only to find one point in this
                                # block of code)
                                exit_flag_second_for_cycle = True

                                break
                        
                        if exit_flag_second_for_cycle:

                            # If we have found the new point, we break the above for cycle
                            break
                        else:
                            pass
            
            # We eliminate the endpoint from the list of remaining points
            border_points_remaining.remove(intersection_point_temp)
        
        output_compute_red_arcs['red_arcs'] = red_arcs
        output_compute_red_arcs['intersection_points_remaining'] = intersection_points_remaining

        return output_compute_red_arcs



def compute_red_circles(regions_input, intersection_points_remaining):

    red_circles = []

    # We now compute the circles 
    while intersection_points_remaining != []:

        # We start a circle from an intersection point not already done, and we remove
        # such point from the list of intersection points remaining
        intersection_point_temp = min(intersection_points_remaining)
        intersection_points_remaining.remove(intersection_point_temp)
        starting_point = intersection_point_temp


        # We construct the circle starting from the border point "intersection_point_temp"
        red_circles.append([intersection_point_temp])

        # Exit flag for the following for cycle
        exit_flag_second_for_cycle = False


        # We find the second point and we append it to the circle
        for region in regions_input:
            if intersection_point_temp in region:
                # we must consider the case in which the intersection point appears more than one 
                # time in the region. We create an array with all the indicies of intersection_point
                region_array = np.array(region)
                searchval = intersection_point_temp
                indicies_of_intersection_point_temp = np.where(region_array == searchval)[0]

                for index in indicies_of_intersection_point_temp:
                    if (index % 2 == 0) and (region[index + 1] in intersection_points_remaining):
                        
                        # We change intersection point and we append this new one to the arc
                        intersection_point_temp = region[index + 1]
                        red_circles[-1].append(intersection_point_temp)

                        # Then we remove this intersection point from the list of remaining
                        # intersection points
                        intersection_points_remaining.remove(intersection_point_temp)

                        # We need to set a flag to exit from the first for cycle, otherwise
                        # the program is going to search also in the remaining regions if it 
                        # can continue the circle (and we want only to find the second point 
                        # in this first block of code)
                        exit_flag_second_for_cycle = True

                        break
                
                if exit_flag_second_for_cycle:
                    break
                else:
                    pass
        

        # We need to understand if we can close the circle or not. We are going to define two controllers: 
        #   - the first one is edge_to_close_the_circle, which is going to be True if we have found 
        #       an edge (which is [intersection_point_temp, starting edge]) that allows us to close 
        #       the circle;
        #   - the second one is intermediate_edge, which is True if we have found an intermediate edge
        #       starting from intersection_point_temp
        # 
        # checked all the other possibilities
        # without finding anything and therefore we can close the circle (after checking that we have indeed 
        # the final edge as a possibility), otherwise is going to be False
        edge_to_close_the_circle = False
        intermediate_edge = False

        # We then iterate the above procedure until we reach the endpoint of the circle, which is the 
        # first point from which we started it
        while not (edge_to_close_the_circle and (not intermediate_edge)):
            
            # We reset the controllers
            edge_to_close_the_circle = False
            intermediate_edge = False

            # Exit flag for the following for cycle
            exit_flag_second_for_cycle = False

            for region in regions_input:

                if intersection_point_temp in region:

                    # we must consider the case in which the intersection point appears more than one 
                    # time in the region. We create an array with all the indicies of intersection_point
                    region_array = np.array(region)
                    searchval = intersection_point_temp
                    indicies_of_intersection_point_temp = np.where(region_array == searchval)[0]
                   
                    for index in indicies_of_intersection_point_temp:
                        if (index % 2 == 0) and (region[index + 1] in intersection_points_remaining):

                            # We change intersection point and we append this new one to the circle
                            # (but we only append it if it is not the starting point)
                            intersection_point_temp = region[index + 1]
                            
                            # We append the new point to the circle
                            red_circles[-1].append(intersection_point_temp)

                            # We remove this intersection point from the list of remaining
                            # intersection points
                            intersection_points_remaining.remove(intersection_point_temp)

                            # We need to set a flag to exit from the first for cycle, otherwise
                            # the program is going to search also in the remaining regions if it 
                            # can continue the circle (and we want only to find one new point in 
                            # this first block of code)
                            exit_flag_second_for_cycle = True

                            # We also set intermediate_edge to True since we have found an intermediate edge
                            intermediate_edge = True

                            break

                        elif (index % 2 == 0) and (region[index + 1] == starting_point):

                            # If we have the possible edge to close the circle, then we set as True
                            # edge_to_close_the_circle
                            edge_to_close_the_circle = True
                    
                    if exit_flag_second_for_cycle:
                        break
                    else:
                        pass



    return red_circles




def compute_blue_circles(regions_input, number_border_points, number_intersection_points):

    blue_circles = []

    # All the intersection points that are not border have to stay on a blue circle
    intersection_points_remaining = list(range(number_border_points +1, number_intersection_points+1))

    # We now compute the circles 
    while intersection_points_remaining != []:

        # We start a circle from an intersection point not already done, and we remove
        # such point from the list of intersection points remaining
        intersection_point_temp = min(intersection_points_remaining)
        intersection_points_remaining.remove(intersection_point_temp)
        starting_point = intersection_point_temp


        # We construct the circle starting from the border point "intersection_point_temp"
        blue_circles.append([intersection_point_temp])

        # Exit flag for the following for cycle
        exit_flag_second_for_cycle = False

        # We find the second point and we append it to the circle
        for region in regions_input:
            if intersection_point_temp in region:
                # we must consider the case in which the intersection point appears more than one 
                # time in the region. We create an array with all the indicies of intersection_point
                region_array = np.array(region)
                searchval = intersection_point_temp
                indicies_of_intersection_point_temp = np.where(region_array == searchval)[0]

                for index in indicies_of_intersection_point_temp:
                    if (index % 2 == 1) and (index != (len(region) - 1)) and (region[index + 1] in intersection_points_remaining):
                        
                        # We change intersection point and we append this new one to the arc
                        intersection_point_temp = region[index + 1]
                        blue_circles[-1].append(intersection_point_temp)

                        # Then we remove this intersection point from the list of remaining
                        # intersection points
                        intersection_points_remaining.remove(intersection_point_temp)

                        # We need to set a flag to exit from the first for cycle, otherwise
                        # the program is going to search also in the remaining regions if it 
                        # can continue the circle (and we want only to find the second point 
                        # in this first block of code)
                        exit_flag_second_for_cycle = True

                        break

                    elif (index == (len(region) - 1)) and (region[0] in intersection_points_remaining):
                        
                        # We change intersection point and we append this new one to the arc
                        intersection_point_temp = region[0]
                        blue_circles[-1].append(intersection_point_temp)

                        # Then we remove this intersection point from the list of remaining
                        # intersection points
                        intersection_points_remaining.remove(intersection_point_temp)

                        # We need to set a flag to exit from the first for cycle, otherwise
                        # the program is going to search also in the remaining regions if it 
                        # can continue the circle (and we want only to find the second point 
                        # in this first block of code)
                        exit_flag_second_for_cycle = True

                        break
                
                if exit_flag_second_for_cycle:
                    break
                else:
                    pass



        # We need to understand if we can close the circle or not. We are going to define two controllers: 
        #   - the first one is edge_to_close_the_circle, which is going to be True if we have found 
        #       an edge (which is [intersection_point_temp, starting edge]) that allows us to close 
        #       the circle;
        #   - the second one is intermediate_edge, which is True if we have found an intermediate edge
        #       starting from intersection_point_temp
        # 
        # checked all the other possibilities
        # without finding anything and therefore we can close the circle (after checking that we have indeed 
        # the final edge as a possibility), otherwise is going to be False
        edge_to_close_the_circle = False
        intermediate_edge = False

        # We then iterate the above procedure until we reach the endpoint of the circle, which is the 
        # first point from which we started it
        while not (edge_to_close_the_circle and (not intermediate_edge)):
            
            # We reset the controllers
            edge_to_close_the_circle = False
            intermediate_edge = False
            
            # Exit flag for the following for cycle
            exit_flag_second_for_cycle = False

            for region in regions_input:

                if intersection_point_temp in region:

                    # we must consider the case in which the intersection point appears more than one 
                    # time in the region. We create an array with all the indicies of intersection_point
                    region_array = np.array(region)
                    searchval = intersection_point_temp
                    indicies_of_intersection_point_temp = np.where(region_array == searchval)[0]
                   
                    for index in indicies_of_intersection_point_temp:
                        if (index % 2 == 1) and (index != (len(region) - 1)) and (region[index + 1] in intersection_points_remaining):

                            # We change intersection point and we append this new one to the circle
                            # (but we only append it if it is not the starting point)
                            intersection_point_temp = region[index + 1]
                            
                            blue_circles[-1].append(intersection_point_temp)

                            # Then we remove this intersection point from the list of remaining
                            # intersection points
                            intersection_points_remaining.remove(intersection_point_temp)

                            # We need to set a flag to exit from the first for cycle, otherwise
                            # the program is going to search also in the remaining regions if it 
                            # can continue the circle (and we want only to find one new point in 
                            # this first block of code)
                            exit_flag_second_for_cycle = True

                            # We also set intermediate_edge to True since we have found an intermediate edge
                            intermediate_edge = True

                            break

                        elif (index == (len(region) - 1)) and (region[0] in intersection_points_remaining):

                            # We change intersection point and we append this new one to the circle
                            # (but we only append it if it is not the starting point)
                            intersection_point_temp = region[0]
                            
                            blue_circles[-1].append(intersection_point_temp)

                            # Then we remove this intersection point from the list of remaining
                            # intersection points
                            intersection_points_remaining.remove(intersection_point_temp)

                            # We need to set a flag to exit from the first for cycle, otherwise
                            # the program is going to search also in the remaining regions if it 
                            # can continue the circle (and we want only to find one new point in 
                            # this first block of code)
                            exit_flag_second_for_cycle = True

                            # We also set intermediate_edge to True since we have found an intermediate edge
                            intermediate_edge = True

                            break
                        
                        elif (index % 2 == 1) and (index != (len(region) - 1)) and (region[index + 1] == starting_point):

                            # If we have the possible edge to close the circle, then we set as True
                            # edge_to_close_the_circle
                            edge_to_close_the_circle = True

                        elif (index == (len(region) - 1)) and (region[0] == starting_point):

                            # If we have the possible edge to close the circle, then we set as True
                            # edge_to_close_the_circle
                            edge_to_close_the_circle = True

                    if exit_flag_second_for_cycle:
                        break
                    else:
                        pass

    return blue_circles



def compute_curves_diagram(regions_input, number_border_points, number_intersection_points):
    curves = dict()

    output_compute_red_arcs = compute_red_arcs(regions_input, number_border_points, number_intersection_points)
    curves['red_arcs'] = output_compute_red_arcs['red_arcs']
    intersection_points_remaining_for_red_circles = output_compute_red_arcs['intersection_points_remaining']
    curves['red_circles'] = compute_red_circles(regions_input, intersection_points_remaining_for_red_circles)
    curves['blue_circles'] = compute_blue_circles(regions_input, number_border_points, number_intersection_points)

    return curves