








# ----------------------------------------------------------------------------------- #
#			*THIS IS A DEVELOP BRANCH, DO NOT USE IT TO RUN THE ALGORITHM*			  #
# ----------------------------------------------------------------------------------- #














#!/usr/bin/env python3


from functions.input_manager import input_manager
from functions.printing_functions import check_the_input, saving_intermediate_steps
from functions.application_algorithm import application_algorithm
from tangles_functions.output_for_computing_invariant import output_for_computing_invariant










# ----------------------------------------------------------------------------------- #
#								INPUT AND PARAMETERS								  #
# ----------------------------------------------------------------------------------- #


# Input

# In the case it is wanted to manually put the in via console, de-comment next line
#inputstream=sys.stdin


# Choose the right path and change eventually the name of the file

#input_path = ("./inputs/normal/", "closed_diagram.txt")
#input_path = ("./inputs/normal/", "bordered_sutured_diagram.txt")

#input_path = ("./inputs/rational/", "rational_tangle.txt")
#input_path = ("./inputs/rational/", "sum_of_rational_tangles.txt")

input_path = ("./inputs/tangles/", "pretzel_tangle.txt")





# Parameters for the run
user_experience = False
input_check = False
try_multiplicity_zero_regions_choices = True

print_distance_complexities = True
print_intermediate_steps = False
print_final_diagram = False
print_details_nicefication = True
print_output_for_PQM = True

save_on_file = True
save_intermediate_steps = True
save_final_diagram = True
save_details_nicefication = True
save_output_for_PQM = True














# ----------------------------------------------------------------------------------- #
#								PRE-PROCESS OF INPUT								  #
# ----------------------------------------------------------------------------------- #


# We save all parameters in a dictionary
parameters_dict = dict()

parameters_dict['user_experience'] = user_experience
parameters_dict['input_check'] = input_check
parameters_dict['try_multiplicity_zero_regions_choices'] = try_multiplicity_zero_regions_choices
parameters_dict['print_distance_complexities'] = print_distance_complexities
parameters_dict['print_intermediate_steps'] = print_intermediate_steps
parameters_dict['print_final_diagram'] = print_final_diagram
parameters_dict['print_details_nicefication'] = print_details_nicefication
parameters_dict['print_output_for_PQM'] = print_output_for_PQM
parameters_dict['save_on_file'] = save_on_file
parameters_dict['save_intermediate_steps'] = save_intermediate_steps
parameters_dict['save_final_diagram'] = save_final_diagram
parameters_dict['save_details_nicefication'] = save_details_nicefication
parameters_dict['save_output_for_PQM'] = save_output_for_PQM



# We read the input
inputstream = open(input_path[0] + input_path[1],'r')

# We distinguish between the different kinds of diagrams that we can have as input and
# we extrapolate the right data for constructing the diagram
input_dictionary = input_manager(inputstream, parameters_dict)

# We close the input file
inputstream.close()



# We save the data from the input
regions_input = input_dictionary['regions_input']
number_border_points = input_dictionary['number_border_points']
number_intersection_points = input_dictionary['number_intersection_points']
alpha_arcs_sites = input_dictionary['alpha_arcs_sites']
alexander_grading = input_dictionary['alexander_grading']
tangle_diagram_flag = input_dictionary['tangle_diagram_flag']
type_of_diagram = input_dictionary['type_of_diagram']

order_for_nicefication = input_dictionary['order_for_nicefication']
possible_diagrams = input_dictionary['possible_diagrams']
best_looking_diagrams = input_dictionary['best_looking_diagrams']




# To optimize the result of the program, we are going to try to move the basepoints of the diagram.
# Therefore, we are going to nicefy all the possible diagrams and then we'll choose the one with the 
# smallest number of generators


minimal_number_generators = -1
index_winner = 0
final_diagram = dict()

# We set a flag to know that we have more than one diagram to try out
more_than_one_diagram = len(order_for_nicefication) > 1




if input_check:

	# Function that allows the user to check that the input given is correct
	check_the_input(parameters_dict, possible_diagrams[0], type_of_diagram)



for index in order_for_nicefication:


	# We take the diagram saved in index
	H_diagram = possible_diagrams[index]





	# We check if our diagram is bordered and, in such case, we check the border regions, 
	# to see if the are already squares or bigons or if we need to do an initial finger 
	# move (and in such case, we do this required finger move)
	H_diagram.finger_move_beginning_bordered(user_experience)












	# ----------------------------------------------------------------------------------- #
	#								SARKAR-WANG ALGORITHM								  #
	# ----------------------------------------------------------------------------------- #


	# The setup is done and we can apply the algorithm to the diagram until it become nice

	print('---------------------------------------------------\n')
	print('		SARKAR-WANG ALGORITHM		\n')
	print('---------------------------------------------------')
	print("\n")
	print("We are now going to run the algorithm on the Heegaard Diagram")
	if user_experience:
		input('\nPress enter to continue...')

	print("\n")


	# We apply the algorithm on H_diagram
	results_algorithm = application_algorithm(parameters_dict, H_diagram, minimal_number_generators, more_than_one_diagram)


	
	# We check if we have a potential final diagram or if we stopped the algorithm 
	# because a previous one has less generators
	new_final_diagram = results_algorithm['new_final_diagram']


	if new_final_diagram:

		# We save the results
		final_diagram['intermediate_steps'] = results_algorithm['intermediate_steps']
		final_diagram['number_iteration_algorithm'] = results_algorithm['number_iteration_algorithm']
		final_diagram['H_diagram'] = results_algorithm['H_diagram']
		final_diagram['number_of_generators'] = H_diagram.number_of_generators
		final_diagram['was_the_one_looking_best_in_the_beginning'] = index in best_looking_diagrams
		index_winner = index

		# We update the new minimal number of generators
		minimal_number_generators = results_algorithm['H_diagram'].number_of_generators





# We save the right final data
intermediate_steps = final_diagram['intermediate_steps']
number_iteration_algorithm = final_diagram['number_iteration_algorithm']
H_diagram = final_diagram['H_diagram']
number_of_generators = final_diagram['number_of_generators']




# ----------------------------------------------------------------------------------- #
#										OUTPUT										  #
# ----------------------------------------------------------------------------------- #

print('\n')
print('The algorithm worked!\n')
print(f'We were able to nicefy the input given in {input_path[0]} for the diagram {input_path[1]}')
print('\n')

if print_details_nicefication:
	
	print(f'Number of generators of the diagram: {number_of_generators}')
	print(f'Number of cycle of the algorithm: {number_iteration_algorithm}')
	print(f'Number of regions of the diagram: {H_diagram.number_of_regions}')
	#print(f"\nWas the diagram between the best looking ones: {final_diagram['was_the_one_looking_best_in_the_beginning']} \n")
	print('\n\n\n')


output_detail_nicefication = f'Number of generators of the diagram: {number_of_generators}\n'
output_detail_nicefication = output_detail_nicefication + f'Number of regions of the diagram: {H_diagram.number_of_regions}\n'
output_detail_nicefication = output_detail_nicefication + f'Number of cycle of the algorithm: {number_iteration_algorithm} \n'
#output_detail_nicefication = output_detail_nicefication + f"\nWas the diagram between the best looking ones: {final_diagram['was_the_one_looking_best_in_the_beginning']}"
output_detail_nicefication = output_detail_nicefication + '\n\n\n\n\n'



#If we are dealing with a 4-endend tangle diagram and the flags are activated, 
# we compute the input for the PQM.m Mathematica Package
if (tangle_diagram_flag) and (print_output_for_PQM or save_output_for_PQM):

	output_string_to_print_PQM, output_string_PQM = output_for_computing_invariant(H_diagram, number_border_points, alpha_arcs_sites, alexander_grading)

	if print_output_for_PQM:

		print("This is the string to copy and paste as PQM.m Mathematica Package input: \n")

		if user_experience:
			input('\nPress enter to continue...')

		print("\n")
		print("\n")

		print(output_string_to_print_PQM)


if print_final_diagram:
	print(H_diagram)


if save_intermediate_steps:
	output_intermediate_steps = saving_intermediate_steps(parameters_dict, intermediate_steps, number_iteration_algorithm)



# If we save on file, we open the outputstram
if save_on_file:

	outputstream = open(input_path[0]+ "nicefied_diagrams/" + input_path[1][:-4] + "_nicefied_diagram.txt",'w+')

	if save_details_nicefication:
		outputstream.write(output_detail_nicefication)

	if (tangle_diagram_flag) and (save_output_for_PQM):
		outputstream.write(output_string_PQM)

	if save_final_diagram:
		outputstream.write(output_intermediate_steps)

	if save_intermediate_steps:
		outputstream.write(output_intermediate_steps)


	outputstream.close()
