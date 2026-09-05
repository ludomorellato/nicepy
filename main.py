#!/usr/bin/env python3


import os

from functions.pipeline import nicefy
from functions.printing_functions import saving_intermediate_steps
from tangles_functions.output_for_computing_invariant import output_for_computing_invariant


# ----------------------------------------------------------------------------------- #
#								INPUT AND PARAMETERS								  #
# ----------------------------------------------------------------------------------- #


# Choose the right path and change eventually the name of the file

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




# ----------------------------------------------------------------------------------- #
#									NICEFICATION									  #
# ----------------------------------------------------------------------------------- #


results = nicefy(input_path[0] + input_path[1], parameters_dict)

H_diagram = results['H_diagram']
intermediate_steps = results['intermediate_steps']
number_iteration_algorithm = results['number_iteration_algorithm']
number_of_generators = results['number_of_generators']

number_border_points = results['number_border_points']
alpha_arcs_sites = results['alpha_arcs_sites']
alexander_grading = results['alexander_grading']
tangle_diagram_flag = results['tangle_diagram_flag']




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
	print('\n\n\n')


output_detail_nicefication = f'Number of generators of the diagram: {number_of_generators}\n'
output_detail_nicefication = output_detail_nicefication + f'Number of regions of the diagram: {H_diagram.number_of_regions}\n'
output_detail_nicefication = output_detail_nicefication + 'Number of cycle of the algorithm: %d \n' %number_iteration_algorithm
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


# We render the intermediate steps of the run. We always bind the string, so that
# the output stage below cannot reach it unbound
output_intermediate_steps = ''

if save_intermediate_steps:
	output_intermediate_steps = saving_intermediate_steps(parameters_dict, intermediate_steps, number_iteration_algorithm)



# If we save on file, we open the outputstram
if save_on_file:

	output_directory = input_path[0] + "nicefied_diagrams/"
	os.makedirs(output_directory, exist_ok=True)

	outputstream = open(output_directory + input_path[1][:-4] + "_nicefied_diagram.txt",'w+')

	if save_details_nicefication:
		outputstream.write(output_detail_nicefication)

	if (tangle_diagram_flag) and (save_output_for_PQM):
		outputstream.write(output_string_PQM)

	if save_final_diagram:
		outputstream.write('\nFINAL DIAGRAM\n')
		outputstream.write(H_diagram.__str__())
		outputstream.write('\n')

	if save_intermediate_steps:
		outputstream.write(output_intermediate_steps)


	outputstream.close()
