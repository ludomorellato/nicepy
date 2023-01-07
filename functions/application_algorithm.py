from copy import deepcopy

from functions.sanity_checks import check_on_the_correctness_of_basepoints_dictionary

from classes.Heegaard_Diagram_class import Heegaard_diagram



def application_algorithm(parameters_dict, H_diagram, minimal_number_generators, more_than_one_diagram):

    print_distance_complexities = parameters_dict['print_distance_complexities']
    print_intermediate_steps = parameters_dict['print_intermediate_steps']
    user_experience = parameters_dict['user_experience']

    # We set a flag to see if we have a new better diagram or if we stopped the cycle
    # because we surpassed the possible minimal number of generators
    new_final_diagram = True 


    # We set a counter to see how many iteration were needed
    number_iteration_algorithm = 0

    # We set a dictionary to keep track of the intermediate steps
    intermediate_steps = dict()

    # We save the initial state of the diagram
    intermediate_steps[0] = Heegaard_diagram(H_diagram.number_intersection_points, H_diagram.number_border_points, deepcopy(H_diagram.regions_input), deepcopy(H_diagram.basepoints_dictionary), [])


    # We set a flag to know that we already notify about the problem of red edges not coinciding on both sides 
    # in the red edges and basepoints dictionary (inside check_on_the_correctness_of_basepoints_dictionary)
    already_notified = False


    # We cycle the algortihm
    while not H_diagram.is_nice:
        
        if print_distance_complexities:
            print('\n')
            print(H_diagram.distance_complexities)
            print(f'Total complexity: {H_diagram.total_complexity}')
            print(f'Number of generators: {H_diagram.number_of_generators}')

        
        # We increase the counter
        number_iteration_algorithm = number_iteration_algorithm + 1

        # We run the algorithm
        H_diagram.Sarkar_Wang_algorithm()

        # We check if does make sense to preceed or if we can stop, by comparing 
        # the number of generators at this step with the minimal number of generators 
        # that we obtained so far
        if more_than_one_diagram and (H_diagram.number_of_generators > minimal_number_generators) and (minimal_number_generators > 0):
            
            # We set the flag to False
            new_final_diagram = False

            # We break the while cycle
            break
        
        
        # If the number of generatos is still below the minimal possible, we can still proceed with the algorithm
        
        # We save the new diagram in the intermediate_steps dictionary
        intermediate_steps[number_iteration_algorithm] = Heegaard_diagram(H_diagram.number_intersection_points, H_diagram.number_border_points, deepcopy(H_diagram.regions_input), deepcopy(H_diagram.basepoints_dictionary), deepcopy(H_diagram.last_diagram_regions_modified))

        #print(H_diagram)
        # We check that the basepoint_and_red_edges dictionary is correct
        check_on_the_correctness_of_basepoints_dictionary(H_diagram, already_notified)


        if print_intermediate_steps:
            print(H_diagram)

        if user_experience:
            input('\nPress enter to continue...')



    # We set up the output
    output = dict()
    output['new_final_diagram'] = new_final_diagram


    if new_final_diagram:
            
        # The last cycle only change the "is_nice" attribute of the diagram
        # We fix the counter of the cycle and the dictionary for the intermediate steps
        number_iteration_algorithm = number_iteration_algorithm - 1
        del intermediate_steps[number_iteration_algorithm + 1]
        intermediate_steps[number_iteration_algorithm] = H_diagram


        # We save the results of this nicefication
        output['intermediate_steps'] = intermediate_steps
        output['number_iteration_algorithm'] = number_iteration_algorithm
        output['H_diagram'] = H_diagram




    return output
