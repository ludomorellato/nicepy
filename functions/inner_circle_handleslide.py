import sys
from functions.get_index_of_edge import get_index_of_edge

# With this function we understand which is the inner circle of an handleslide

def inner_circle_handleslide(diagram, starting_region_label, regions_to_go_through, edges_to_go_through):
    
    # We try to understand which blue circle is the one that we are sliding on, by
    # understanding which circle is in the middle of the first and the last red
    # edges that we cut through
    first_edge_index = get_index_of_edge(diagram.regions[starting_region_label].input, edges_to_go_through[0])
    last_edge_index = get_index_of_edge(diagram.regions[starting_region_label].input, edges_to_go_through[-1][::-1])
    
    # We extrapolate the blue edge
    minimal_index = min(first_edge_index, last_edge_index)
    maximal_index = max(first_edge_index, last_edge_index)

    if minimal_index == 0 and maximal_index != 2:
        
        minimal_index_is_start =(minimal_index == first_edge_index)
        blue_edge = [diagram.regions[starting_region_label].input[-1], diagram.regions[starting_region_label].input[0]]
    
    else:
        
        minimal_index_is_start = (minimal_index == first_edge_index)
        blue_edge = diagram.regions[starting_region_label].input[minimal_index + 1: maximal_index + 1]

    if len(blue_edge) != 2:
        sys.exit('Error: in the search for the inner handleslide, we found a blue edge which is not an edge (it is not long 2).')

    # We now consider all the blue circles
    blue_circles = diagram.blue_circles

    # We search for the right circle
    for circle in blue_circles:

        # We zip the circle
        circle_zipped = list(map(list, zip(circle, circle[1:]+ [circle[0]])))

        # We look if blue_edge is in circle_zipped
        if blue_edge in circle_zipped:
            
            # We return this circle zipped in the right direction
            if minimal_index_is_start:

                # In this case, the direction is already correct
                return circle_zipped

            else:

                # In this case, the circle is going to be needed in the other direction
                circle = circle[::-1]
                circle_zipped = list(map(list, zip(circle, circle[1:]+ [circle[0]])))
                
                return circle_zipped
        
        elif blue_edge[::-1] in circle_zipped:

            # We return this circle zipped in the right direction
            if minimal_index_is_start:

                # In this case, the circle is going to be needed in the other direction
                circle = circle[::-1]
                circle_zipped = list(map(list, zip(circle, circle[1:]+ [circle[0]])))
                
                return circle_zipped

            else:

                # In this case, the direction is already correct
                return circle_zipped
                

        else:

            # It is not the right circle, we pass to the next one
            pass