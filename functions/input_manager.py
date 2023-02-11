import string
from copy import deepcopy
import sys

from functions.input_purifier import list_of_list_input, list_input, string_input
from functions.sanity_checks import check_no_circle_one_or_two_points
from functions.compute_circles_and_arcs import compute_curves_diagram

from classes.Heegaard_Diagram_class import Heegaard_diagram

from tangles_functions.close_4_ended_tangle_diagram import close_4_ended_tangle_diagram
from tangles_functions.rational_tangles_input import heegaard_diagram_for_rational_tangle
from tangles_functions.glue_rational_tangles import glue_rational_tangles



















def input_manager(inputstream, parameters_dict):

    type_of_diagram = inputstream.readline().translate({ord(c): None for c in string.whitespace})


    if (type_of_diagram.lower() == 'normal') or (type_of_diagram.lower()  == 'tangle'):

        return normal_or_tangle_diagram(inputstream, type_of_diagram, parameters_dict)



    if type_of_diagram.lower() == 'rational':
        
        return rational_diagram(inputstream, type_of_diagram, parameters_dict)

































def normal_or_tangle_diagram(inputstream, type_of_diagram, parameters_dict):

    try_multiplicity_zero_regions_choices = parameters_dict['try_multiplicity_zero_regions_choices']

    number_border_points = int(inputstream.readline())
    number_intersection_points = int(inputstream.readline())
    regions_input = list_of_list_input(inputstream.readline())
    


    # First off, we do a sanity check on the input
    # We compute now the lists of lists that describe the alpha arcs, the alpha circles and the blue circles
    curves_diagram = compute_curves_diagram(regions_input, number_border_points, number_intersection_points)

    red_arcs = curves_diagram['red_arcs']
    red_circles = curves_diagram['red_circles']
    blue_circles = curves_diagram['blue_circles']



    # Now we check if we have circles with only one or two points on them;
    # in such case we ask to do a finger move to remove this problem
    check_no_circle_one_or_two_points(red_circles, blue_circles)





    # We set a flag to know whether it is a 4-ended tangle diagram or not
    if type_of_diagram.lower()  == 'tangle':
        tangle_diagram_flag = True
    else:
        tangle_diagram_flag = False


    # We contruct a dictionary with all the information about basepoints
    basepoints_dictionary = dict()

    if tangle_diagram_flag:
        # If we are dealing with a 4-ended tangle diagram, the next line is list of lists
        multiplicity_zero_regions = list_of_list_input(inputstream.readline())
        alpha_arcs_sites = list_input(inputstream.readline())
        alexander_grading = list_input(inputstream.readline())

        basepoints_dictionary['multiplicity_zero_regions'] = [couple[0] for couple in multiplicity_zero_regions]
        basepoints_dictionary['p_or_q'] = multiplicity_zero_regions
        basepoints_dictionary['basepoint_regions_and_red_edges'] = dict()


        # We set the output
        output_dictionary = dict()

        output_dictionary['regions_input'] = regions_input
        output_dictionary['number_border_points'] = number_border_points
        output_dictionary['number_intersection_points'] = number_intersection_points
        output_dictionary['alpha_arcs_sites'] = alpha_arcs_sites
        output_dictionary['alexander_grading'] = alexander_grading
        output_dictionary['tangle_diagram_flag'] = tangle_diagram_flag
        output_dictionary['type_of_diagram'] = type_of_diagram

        


        if try_multiplicity_zero_regions_choices:
                
            # We define the first Heegaard diagram, so that we can also study all the other 
            # possibilities in the basepoints placement
            # We define the class Heegaard_diagram for this diagram. Within this definiton,
            # we generate the regions as classes, we compute the lists of lists of circles and arcs
            # we do a first sanity check and we compute neighbours and distances for every region.
            first_diagram = Heegaard_diagram(number_intersection_points, number_border_points, regions_input, basepoints_dictionary, False)

            multiple_basepoints_dictionaries = find_possible_mulitplicity_zero_regions(first_diagram)


            # We create the diagrams and we decide which one is the best one to work on
            possible_diagrams = dict()


            # We create the first one by hand
            possible_diagrams[0] = Heegaard_diagram(number_intersection_points, number_border_points, deepcopy(regions_input), multiple_basepoints_dictionaries[0], False)



            # We close it: we want to eliminate the borders and 
            # obtain an alpha circle instead of four alpha arcs. We also generate new basepoints
            # that count more than 0 in the sense of the multiplicity where we close the borders
            # (in the case in which we don't have a multiplicity zero basepoint in such region)
            close_4_ended_tangle_diagram(possible_diagrams[0])



            # We save the data of the minimal diagram
            # We use this diagram as the first minimum    
            minimal_total_complexity = possible_diagrams[0].total_complexity
            minimal_diagram_indicies = [0]

            # We create the list of the discarded indicies
            discarded_indices = []


            # We create all the others diagrams and we compare the sum of the total badness to the minimum one
            for index in range(1, 16):
                possible_diagrams[index] = Heegaard_diagram(number_intersection_points, number_border_points, deepcopy(regions_input), multiple_basepoints_dictionaries[index], False)
                


                # We close it: we want to eliminate the borders and 
                # obtain an alpha circle instead of four alpha arcs. We also generate new basepoints
                # that count more than 0 in the sense of the multiplicity where we close the borders
                # (in the case in which we don't have a multiplicity zero basepoint in such region)
                close_4_ended_tangle_diagram(possible_diagrams[index])



                # We check if we have a new minimal sum of total badness
                if possible_diagrams[index].total_complexity < minimal_total_complexity:

                    # We save the bad indicies in the discarded_indicies list
                    discarded_indices = discarded_indices + minimal_diagram_indicies

                    # We reset the list of indicies of minimum badness
                    minimal_diagram_indicies = [index]
                    minimal_total_complexity = possible_diagrams[index].total_complexity

                # We check if this is another diagram with the same sum of total badness
                elif possible_diagrams[index].total_complexity == minimal_total_complexity:

                    minimal_diagram_indicies.append(index)

                # In all the other cases, we append this index in the discarded_indices list
                else:
                    
                    discarded_indices.append(index)


            # We create a list with the right order for trying to nicefy all the 16 possible diagrams
            output_dictionary['order_for_nicefication'] = minimal_diagram_indicies + discarded_indices


            # We give out all the diagrams already initialized
            output_dictionary['possible_diagrams'] = possible_diagrams

            # We save the data of the indicies of the best looking diagrams
            output_dictionary['best_looking_diagrams'] = minimal_diagram_indicies


            return output_dictionary



        else:

            # We define only the Heegaard diagram given as input.
            # We define the class Heegaard_diagram for this diagram. Within this definiton,
            # we generate the regions as classes, we compute the lists of lists of circles and arcs
            # we do a first sanity check and we compute neighbours and distances for every region.
            diagram = Heegaard_diagram(number_intersection_points, number_border_points, regions_input, basepoints_dictionary, False)


            # We put it into a dictionary
            diagram_dictionary = dict()
            diagram_dictionary[0] = diagram



            # We close it: we want to eliminate the borders and 
            # obtain an alpha circle instead of four alpha arcs. We also generate new basepoints
            # that count more than 0 in the sense of the multiplicity where we close the borders
            # (in the case in which we don't have a multiplicity zero basepoint in such region)
            close_4_ended_tangle_diagram(possible_diagrams[0])


            # We create a list with only the index for the unique diagram
            output_dictionary['order_for_nicefication'] = [0]

            # We give out the diagram
            output_dictionary['possible_diagrams'] = diagram_dictionary

            # We save the data of the unique index of this diagram
            output_dictionary['best_looking_diagrams'] = [0]


            return output_dictionary





    else:
        # In this other case, it is just a list
        multiplicity_zero_regions = list_input(inputstream.readline())

        basepoints_dictionary['multiplicity_zero_regions'] = multiplicity_zero_regions
        basepoints_dictionary['p_or_q'] = False
        basepoints_dictionary['basepoint_regions_and_red_edges'] = False

        # For trying more position for the basepoint (NOT YET IMPLEMENTED)
        multiple_basepoints_dictionaries = dict()
        multiple_basepoints_dictionaries[0] = basepoints_dictionary

        # We set the output
        output_dictionary = dict()

        output_dictionary['regions_input'] = regions_input
        output_dictionary['number_border_points'] = number_border_points
        output_dictionary['number_intersection_points'] = number_intersection_points
        output_dictionary['alpha_arcs_sites'] = None
        output_dictionary['alexander_grading'] = None
        output_dictionary['tangle_diagram_flag'] = tangle_diagram_flag
        output_dictionary['type_of_diagram'] = type_of_diagram


        # We define the class Heegaard_diagram for this diagram. Within this definiton,
        # we generate the regions as classes, we compute the lists of lists of circles and arcs
        # we do a first sanity check and we compute neighbours and distances for every region.
        diagram = Heegaard_diagram(number_intersection_points, number_border_points, deepcopy(regions_input), multiple_basepoints_dictionaries[0], False)
        
        # We give out the diagram and the list of the order for the nicefications (i.e. only the index 0 in this case)
        output_dictionary['possible_diagrams'] = {0: diagram}
        output_dictionary['order_for_nicefication'] = [0]
        output_dictionary['best_looking_diagrams'] = [0]


    return output_dictionary





































def rational_diagram(inputstream, type_of_diagram, parameters_dict):

    number_of_tangles = int(inputstream.readline())
    tangles_input = list_of_list_input(inputstream.readline())
    gluing_instructions = list_of_list_input(inputstream.readline())
    alexander_grading_tangle = list_input(inputstream.readline())
    
    # First, we construct the Heegaard diagrams for all the tangles and we dave them in a dictionary
    diagrams_tangles = dict()

    # To not have common labels on intersection points (border points excluded), we set this new variable called
    # label to skip, that keeps track of how many labels we already used for intersection points
    label_to_skip = 0

    for index in range(len(tangles_input)):

        tangle = tangles_input[index]
        sign = tangle[0]*'+' + (1 - tangle[0])*'-'
        p = tangle[1]
        q = tangle[2]

        # We run the function
        output_temp = heegaard_diagram_for_rational_tangle(sign, p, q, label_to_skip)

        # We take the new data from the output
        border_regions = output_temp['border_regions']
        regions_input = output_temp['regions_input']
        label_to_skip = output_temp['label_to_skip']

        # We save the new data in the dictionary
        diagrams_tangles[index + 1] = [regions_input, border_regions]

    # We save the informations on the intersection points
    number_border_points = 8
    number_intersection_points = label_to_skip + 8
    


    # We glue all the pieces together
    glued_tangle_dictionary = glue_rational_tangles(diagrams_tangles, gluing_instructions, tangles_input)

    regions_input = glued_tangle_dictionary['glued_tangle_input']
    possible_multiplicity_zero_regions = glued_tangle_dictionary['possible_multiplicity_zero_regions']

    
    # Sanity check
    if len(possible_multiplicity_zero_regions) > 16:
        sys.exit('Error: we have found more than 16 combinations for the mulitplicity zero regions palcements')


    # We create a dictionary with all the possible basepoints dictionary
    multiple_basepoints_dictionaries = dict()

    for index in range(16):

    # We prepare the basepoint_dictionary's
        multiple_basepoints_dictionaries[index] = dict()
        multiple_basepoints_dictionaries[index]['multiplicity_zero_regions'] = [couple[0] for couple in possible_multiplicity_zero_regions[index]]
        multiple_basepoints_dictionaries[index]['p_or_q'] = possible_multiplicity_zero_regions[index]
        multiple_basepoints_dictionaries[index]['basepoint_regions_and_red_edges'] = dict()
        
    tangle_diagram_flag = True

    # We construct the order of the alpha arcs sites
    alpha_arcs_sites = [2, 4, 6, 8]

    # We fix the alexander gradings
    alexander_grading = []

    for end_point in alexander_grading_tangle:

        # We just need to distinguish between odd and even numbers in the following way
        if end_point % 2 == 1:

            alexander_grading.append(end_point*2)
        else:

            alexander_grading.append(end_point*2 - 1)



    output_dictionary = dict()

    output_dictionary['regions_input'] = regions_input
    output_dictionary['number_border_points'] = number_border_points
    output_dictionary['number_intersection_points'] = number_intersection_points
    output_dictionary['alpha_arcs_sites'] = alpha_arcs_sites
    output_dictionary['alexander_grading'] = alexander_grading
    output_dictionary['tangle_diagram_flag'] = tangle_diagram_flag
    output_dictionary['type_of_diagram'] = type_of_diagram




    # We do a sanity check on the input
    # We compute now the lists of lists that describe the alpha arcs, the alpha circles and the blue circles
    curves_diagram = compute_curves_diagram(regions_input, number_border_points, number_intersection_points)

    red_arcs = curves_diagram['red_arcs']
    red_circles = curves_diagram['red_circles']
    blue_circles = curves_diagram['blue_circles']



    # Now we check if we have circles with only one or two points on them;
    # in such case we ask to do a finger move to remove this problem
    check_no_circle_one_or_two_points(red_circles, blue_circles)




    # We create the diagrams and we decide which one is the best one to work on at first, to set a baseline for the possible number of generators
    possible_diagrams = dict()


    # We create the first diagram by hand
    # We define the class Heegaard_diagram for this diagram. Within this definiton,
	# we generate the regions as classes, we compute the lists of lists of circles and arcs
	# we do a first sanity check and we compute neighbours and distances for every region.
    possible_diagrams[0] = Heegaard_diagram(number_intersection_points, number_border_points, deepcopy(regions_input), multiple_basepoints_dictionaries[0], False)


    # We close it: we want to eliminate the borders and 
    # obtain an alpha circle instead of four alpha arcs. We also generate new basepoints
    # that count more than 0 in the sense of the multiplicity where we close the borders
    # (in the case in which we don't have a multiplicity zero basepoint in such region)
    close_4_ended_tangle_diagram(possible_diagrams[0])

    
    # We save the data of the minimal diagram
    # We use this diagram as the first minimum    
    minimal_total_complexity = possible_diagrams[0].total_complexity
    minimal_diagram_indicies = [0]

    # We create the list of the discarded indicies
    discarded_indices = []


    # We create all the others diagrams and we compare the sum of the total badness to the minimum one
    for index in range(1, 16):
        possible_diagrams[index] = Heegaard_diagram(number_intersection_points, number_border_points, deepcopy(regions_input), multiple_basepoints_dictionaries[index], False)
        


        # We close it: we want to eliminate the borders and 
        # obtain an alpha circle instead of four alpha arcs. We also generate new basepoints
        # that count more than 0 in the sense of the multiplicity where we close the borders
        # (in the case in which we don't have a multiplicity zero basepoint in such region)
        close_4_ended_tangle_diagram(possible_diagrams[index])


        # We check if we have a new minimal sum of total badness
        if possible_diagrams[index].total_complexity < minimal_total_complexity:
            
            # We save the bad indicies in the discarded_indicies list
            discarded_indices = discarded_indices + minimal_diagram_indicies

            # We reset the list of indicies of minimum badness
            minimal_diagram_indicies = [index]
            minimal_total_complexity = possible_diagrams[index].total_complexity

        # We check if this is another diagram with the same sum of total badness
        elif possible_diagrams[index].total_complexity == minimal_total_complexity:

            minimal_diagram_indicies.append(index)

        # In all the other cases, we append this index in the discarded_indices list
        else:
            
            discarded_indices.append(index)


    # We create a list with the right order for trying to nicefy all the 16 possible diagrams
    output_dictionary['order_for_nicefication'] = minimal_diagram_indicies + discarded_indices


    # We give out all the diagrams already initialized
    output_dictionary['possible_diagrams'] = possible_diagrams

    
    # We save the data of the indicies of the best looking diagrams
    output_dictionary['best_looking_diagrams'] = minimal_diagram_indicies


    return output_dictionary






























def find_possible_mulitplicity_zero_regions(diagram):

    internal_border_regions = []
    external_border_regions = []

    # We look thorugh the border regions and we find if they are internal or external
    for region_index in diagram.border_regions:
        
        region = diagram.regions[region_index]

        if region.p_or_q == 'p':

            internal_border_regions.append(region_index)

        else: 

            external_border_regions.append(region_index)


    # We create a dictionary with all the possible basepoints dictionary
    possible_basepoints_dictionary = dict()

    counter = 0

    for int_region in internal_border_regions:

        for ext_region in external_border_regions:

            # We prepare the basepoint_dictionary's
            possible_basepoints_dictionary[counter] = dict()
            possible_basepoints_dictionary[counter]['multiplicity_zero_regions'] = [int_region, ext_region]
            possible_basepoints_dictionary[counter]['p_or_q'] = [[int_region, 0], [ext_region, 1]]
            possible_basepoints_dictionary[counter]['basepoint_regions_and_red_edges'] = dict()

            counter = counter + 1


    return possible_basepoints_dictionary