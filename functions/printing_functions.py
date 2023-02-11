



def check_the_input(parameters_dict, diagram, type_of_diagram):

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





def saving_intermediate_steps(parameters_dict, intermediate_steps, number_iteration_algorithm):

    save_final_diagram = parameters_dict['save_final_diagram']

    output = ''

    output = output + '\n'

    if save_final_diagram:
        output = output + 'These are the intermediate step, including the starting diagram and the finishing one:\n'

    else:
        output = output + 'These are the intermediate step, including the starting diagram:\n'

    for step_number in intermediate_steps.keys():
        output = output + '-----------------------------------------------------------------------------'
        output = output + '\n'
        output = output + '\n'

        if step_number == 0:
            output = output + f'Step number {step_number}:	STARTING DIAGRAM \n'
        elif step_number == number_iteration_algorithm:
            output = output + f'Step number {step_number}:	FINAL DIAGRAM \n'
        else:
            output = output + f'Step number {step_number}: \n'
        
        output = output + intermediate_steps[step_number].__str__()
        output = output + '\n'
        output = output + '\n'

    return output
    