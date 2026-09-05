from __future__ import annotations

from typing import Any
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from classes.Heegaard_Diagram_class import Heegaard_diagram





def check_the_input(parameters_dict: dict[str, Any], diagram: Heegaard_diagram, type_of_diagram: str) -> None:

    user_experience = parameters_dict['user_experience']

    if type_of_diagram != 'rational':

        # Sanity check for the user that the input is right
        print("\n")
        print('----------------------------------------------------\n')
        print('		INPUT RECEIVED		\n')
        print('----------------------------------------------------')
        print("The following is the input given")
        print("Check if there are mistakes")

        
        if user_experience:
            input('\nPress enter to continue...')

        print("\n")
        print("\n")
        for i in diagram.regions.keys():
            print(diagram.regions[i])
        print("\n")
        print("\n")

        
        if user_experience:
            input('\nPress enter to continue...')

    else:
        print("\n")
        print('----------------------------------------------------\n')
        print('		INPUT RECEIVED		\n')
        print('----------------------------------------------------')
        print("We have constructed the (gluing of) rational diagram(s) desired")
        
        
        

        print("\n")
        print("\n")
        for i in diagram.regions.keys():
            print(diagram.regions[i])
        print("\n")
        print("\n")
        
        if user_experience:
            input('\nPress enter to continue...')





def saving_intermediate_steps(parameters_dict: dict[str, Any], intermediate_steps: dict[int, Heegaard_diagram], number_iteration_algorithm: int) -> str:
    """Render the diagrams produced at each step of a nicefication run as text.

    Takes the run parameters and the dictionary mapping step number to diagram;
    returns the string to write to the output file. When the final diagram is
    saved separately, the last step is left out so that it is not written twice.
    """

    save_final_diagram = parameters_dict['save_final_diagram']

    # The last intermediate step *is* the final diagram. When that is written on
    # its own we stop one step short, so that it does not appear twice
    if save_final_diagram:
        step_numbers = [step for step in intermediate_steps if step != number_iteration_algorithm]
    else:
        step_numbers = list(intermediate_steps)

    # A run that was already nice has the starting diagram as its only step, so
    # there is nothing left to report once the final diagram is written
    if not step_numbers:
        return ''

    output = ''

    output = output + '\n'

    if save_final_diagram:
        output = output + 'These are the intermediate steps, up to but excluding the final diagram written above:\n'

    else:
        output = output + 'These are the intermediate step, including the starting diagram and the finishing one:\n'

    for step_number in step_numbers:
        output = output + '-----------------------------------------------------------------------------'
        output = output + '\n'
        output = output + '\n'

        if step_number == 0:
            output = output + 'Step number %d:\tSTARTING DIAGRAM \n' %step_number
        elif step_number == number_iteration_algorithm:
            output = output + 'Step number %d:\tFINAL DIAGRAM \n' %step_number
        else:
            output = output + 'Step number %d: \n' %step_number

        output = output + intermediate_steps[step_number].__str__()
        output = output + '\n'
        output = output + '\n'

    return output
