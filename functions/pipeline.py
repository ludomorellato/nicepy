from __future__ import annotations

from typing import Any
from pathlib import Path

from functions.input_manager import input_manager
from functions.printing_functions import check_the_input
from functions.application_algorithm import application_algorithm


def nicefy(input_path: str | Path, parameters_dict: dict[str, Any]) -> dict[str, Any]:
    """Run the Sarkar-Wang nicefication on the diagram described by a file.

    Takes the path of an input file and the dictionary of run parameters, and
    returns a dictionary describing the nicefied diagram: the final
    Heegaard_diagram under 'H_diagram', the diagram at each step under
    'intermediate_steps', the counts reported to the user, and the pieces of the
    input that the caller needs to write the output (the border points, the
    alpha arc sites, the Alexander grading and the kind of diagram).

    For a 4-ended tangle diagram there are several admissible placements of the
    basepoints. We nicefy them in order of increasing complexity and keep the
    one that yields the fewest generators.
    """

    user_experience = parameters_dict['user_experience']
    input_check = parameters_dict['input_check']
    verbose = parameters_dict.get('verbose', False)

    # We read the input
    inputstream = open(input_path, 'r')

    # We distinguish between the different kinds of diagrams that we can have as
    # input and we extrapolate the right data for constructing the diagram
    input_dictionary = input_manager(inputstream, parameters_dict)

    # We close the input file
    inputstream.close()

    # We save the data from the input
    type_of_diagram = input_dictionary['type_of_diagram']
    order_for_nicefication = input_dictionary['order_for_nicefication']
    possible_diagrams = input_dictionary['possible_diagrams']

    # To optimize the result of the program, we are going to try to move the
    # basepoints of the diagram. Therefore, we are going to nicefy all the
    # possible diagrams and then we'll choose the one with the smallest number
    # of generators

    minimal_number_generators = -1
    index_winner = 0
    final_diagram = dict()

    # We set a flag to know that we have more than one diagram to try out
    more_than_one_diagram = len(order_for_nicefication) > 1

    if input_check:

        # Function that allows the user to check that the input given is correct
        check_the_input(parameters_dict, possible_diagrams[0], type_of_diagram)

    # ----------------------------------------------------------------------- #
    #                          SARKAR-WANG ALGORITHM                           #
    # ----------------------------------------------------------------------- #

    # The setup is done and we can apply the algorithm to each diagram until it
    # becomes nice

    if verbose:
        print('---------------------------------------------------\n')
        print('		SARKAR-WANG ALGORITHM		\n')
        print('---------------------------------------------------')
        print("\n")
        print("We are now going to run the algorithm on the Heegaard Diagram")

        if more_than_one_diagram:
            print(f'There are {len(order_for_nicefication)} admissible basepoint placements to try')

        if user_experience:
            input('\nPress enter to continue...')

        print("\n")

    for position, index in enumerate(order_for_nicefication, start=1):

        if verbose and more_than_one_diagram:
            print(f'Basepoint placement {position} of {len(order_for_nicefication)}')

        # We take the diagram saved in index
        H_diagram = possible_diagrams[index]

        # We check if our diagram is bordered and, in such case, we check the
        # border regions, to see if they are already squares or bigons or if we
        # need to do an initial finger move (and in such case, we do this
        # required finger move)
        H_diagram.finger_move_beginning_bordered(user_experience, verbose)

        # We apply the algorithm on H_diagram
        results_algorithm = application_algorithm(parameters_dict, H_diagram, minimal_number_generators, more_than_one_diagram)

        # We check if we have a potential final diagram or if we stopped the
        # algorithm because a previous one has less generators
        new_final_diagram = results_algorithm['new_final_diagram']

        if new_final_diagram:

            # We save the results
            final_diagram['intermediate_steps'] = results_algorithm['intermediate_steps']
            final_diagram['number_iteration_algorithm'] = results_algorithm['number_iteration_algorithm']
            final_diagram['H_diagram'] = results_algorithm['H_diagram']
            final_diagram['number_of_generators'] = H_diagram.number_of_generators
            index_winner = index

            # We update the new minimal number of generators
            minimal_number_generators = results_algorithm['H_diagram'].number_of_generators

    # We save the right final data
    H_diagram = final_diagram['H_diagram']

    # We set up the output
    output = dict()

    output['H_diagram'] = H_diagram
    output['intermediate_steps'] = final_diagram['intermediate_steps']
    output['number_iteration_algorithm'] = final_diagram['number_iteration_algorithm']
    output['number_of_generators'] = final_diagram['number_of_generators']
    output['number_of_regions'] = H_diagram.number_of_regions
    output['index_winner'] = index_winner

    # The parts of the input that the caller needs to write the output
    output['number_border_points'] = input_dictionary['number_border_points']
    output['alpha_arcs_sites'] = input_dictionary['alpha_arcs_sites']
    output['alexander_grading'] = input_dictionary['alexander_grading']
    output['tangle_diagram_flag'] = input_dictionary['tangle_diagram_flag']
    output['type_of_diagram'] = type_of_diagram

    return output
