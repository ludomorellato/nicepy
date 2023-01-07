import sys
from functions.get_index_of_edge import get_index_of_edge

# With this function we understand which is the inner circle of an handleslide

def inner_circle_handleslide_slow(diagram, starting_region_label, regions_to_go_through, edges_to_go_through):
    
    blue_circles = diagram.blue_circles

    circles_zipped = dict()
    circles_found_dict = dict()

    for index in range(len(blue_circles)):
        
        # We compute all the edge of the blue circle in the given order
        circles_zipped[index + 1] = list(map(list, zip(blue_circles[index], blue_circles[index][1:]+ [blue_circles[index][0]])))

        # And in the opposite order
        circles_zipped[-index - 1] = list(map(list, zip(blue_circles[index][::-1], blue_circles[index][:-1][::-1]+ [blue_circles[index][-1]])))

        # We create a list with all the indicies with which we keep track of what we find
        circles_found_dict[index + 1] = []
        circles_found_dict[-index - 1] = []

    # We add the starting region to the regions to analize
    regions_to_go_through = [starting_region_label] + regions_to_go_through

    # The following snippet of code is not really smart, it can be more fast by checking
    # only the circles that we have found in all the previous step (if we miss one at one 
    # step, surely it's not the inner circle)
    for label in regions_to_go_through:

        for blue_edge in diagram.regions[label].blue_edges:
             
             for index in circles_zipped.keys():

                if blue_edge in circles_zipped[index]:

                    # We compose the circle in another dictionary to verify that
                    # indeed we are finding all the circle
                    circles_found_dict[index].append(blue_edge)

        # We overwrite the list of indicies found for the next cycle
        # circles_found = circles_found_temp

    # We create a list of inner circles (it should be only one)
    inner_circle = []

    for index in circles_found_dict.keys():
        circles_found_dict[index].sort()
        circles_zipped[index].sort()

        if circles_found_dict[index] == circles_zipped[index]:
            inner_circle.append(index)

    if len(inner_circle) != 1:
        sys.exit('Error: we found more than one inner circle')
    else:
        return circles_found_dict[inner_circle[0]]