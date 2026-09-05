#!/usr/bin/env python3

"""Nicefy a Heegaard diagram with the Sarkar-Wang algorithm.

Reads a diagram description from a file, applies the algorithm until every
region away from the basepoints is a bigon or a square, and reports the
resulting diagram. See the README for the input format.
"""

import argparse
import sys
from pathlib import Path

from functions.pipeline import nicefy
from functions.printing_functions import saving_intermediate_steps
from tangles_functions.output_for_computing_invariant import output_for_computing_invariant


def build_parser():
	"""Return the argument parser for the command line interface."""

	parser = argparse.ArgumentParser(
		prog='nicepy',
		description=__doc__,
		formatter_class=argparse.RawDescriptionHelpFormatter,
		epilog='example:\n  python main.py inputs/tangles/pretzel_tangle.txt --output out.txt',
	)

	parser.add_argument(
		'input_path',
		metavar='INPUT',
		type=Path,
		help='file describing the Heegaard diagram to nicefy',
	)
	parser.add_argument(
		'-o', '--output',
		metavar='PATH',
		type=Path,
		default=None,
		help='where to write the nicefied diagram '
		     '(default: INPUT_DIR/nicefied_diagrams/INPUT_STEM_nicefied_diagram.txt)',
	)

	run = parser.add_argument_group('run')
	run.add_argument(
		'-v', '--verbose',
		dest='verbose',
		action='store_true',
		help='narrate the run: the initial finger moves and the basepoint '
		     'placement being tried',
	)
	run.add_argument(
		'--interactive',
		dest='user_experience',
		action='store_true',
		help='pause between steps and wait for the return key',
	)
	run.add_argument(
		'--check-input',
		dest='input_check',
		action='store_true',
		help='print the diagram as it was parsed, before running the algorithm',
	)
	run.add_argument(
		'--try-basepoint-placements',
		dest='try_multiplicity_zero_regions_choices',
		action=argparse.BooleanOptionalAction,
		default=True,
		help='for a 4-ended tangle diagram, nicefy every admissible basepoint '
		     'placement and keep the one with the fewest generators (default: enabled)',
	)

	printing = parser.add_argument_group('printing')
	printing.add_argument(
		'--print-details',
		dest='print_details_nicefication',
		action=argparse.BooleanOptionalAction,
		default=True,
		help='print the generator, region and cycle counts (default: enabled)',
	)
	printing.add_argument(
		'--print-distance-complexities',
		dest='print_distance_complexities',
		action=argparse.BooleanOptionalAction,
		default=False,
		help='print the distance complexities at every cycle (verbose)',
	)
	printing.add_argument(
		'--print-intermediate-steps',
		dest='print_intermediate_steps',
		action=argparse.BooleanOptionalAction,
		default=False,
		help='print the diagram after every cycle (verbose)',
	)
	printing.add_argument(
		'--print-final-diagram',
		dest='print_final_diagram',
		action=argparse.BooleanOptionalAction,
		default=False,
		help='print the nicefied diagram in full',
	)
	printing.add_argument(
		'--print-pqm',
		dest='print_output_for_PQM',
		action=argparse.BooleanOptionalAction,
		default=True,
		help='for a tangle diagram, print the input for the PQM.m Mathematica '
		     'package (default: enabled)',
	)

	saving = parser.add_argument_group('saving')
	saving.add_argument(
		'--save',
		dest='save_on_file',
		action=argparse.BooleanOptionalAction,
		default=True,
		help='write the results to the output file (default: enabled)',
	)
	saving.add_argument(
		'--save-details',
		dest='save_details_nicefication',
		action=argparse.BooleanOptionalAction,
		default=True,
		help='include the generator, region and cycle counts (default: enabled)',
	)
	saving.add_argument(
		'--save-final-diagram',
		dest='save_final_diagram',
		action=argparse.BooleanOptionalAction,
		default=True,
		help='include the nicefied diagram (default: enabled)',
	)
	saving.add_argument(
		'--save-intermediate-steps',
		dest='save_intermediate_steps',
		action=argparse.BooleanOptionalAction,
		default=True,
		help='include the diagram at every cycle (default: enabled)',
	)
	saving.add_argument(
		'--save-pqm',
		dest='save_output_for_PQM',
		action=argparse.BooleanOptionalAction,
		default=True,
		help='for a tangle diagram, include the input for the PQM.m Mathematica '
		     'package (default: enabled)',
	)

	return parser


def default_output_path(input_path):
	"""Return where the nicefied diagram of an input file is written by default."""

	return input_path.parent / 'nicefied_diagrams' / (input_path.stem + '_nicefied_diagram.txt')


def main(argv=None):

	parser = build_parser()
	args = parser.parse_args(argv)

	# Everything except the two paths is a run parameter
	parameters_dict = vars(args).copy()
	input_path = parameters_dict.pop('input_path')
	output_path = parameters_dict.pop('output')

	if not input_path.is_file():
		parser.error(f'no such input file: {input_path}')

	if output_path is None:
		output_path = default_output_path(input_path)


	# ------------------------------------------------------------------------- #
	#									NICEFICATION							  #
	# ------------------------------------------------------------------------- #

	results = nicefy(input_path, parameters_dict)

	H_diagram = results['H_diagram']
	intermediate_steps = results['intermediate_steps']
	number_iteration_algorithm = results['number_iteration_algorithm']
	number_of_generators = results['number_of_generators']

	number_border_points = results['number_border_points']
	alpha_arcs_sites = results['alpha_arcs_sites']
	alexander_grading = results['alexander_grading']
	tangle_diagram_flag = results['tangle_diagram_flag']


	# ------------------------------------------------------------------------- #
	#										OUTPUT								  #
	# ------------------------------------------------------------------------- #

	print('\n')
	print('The algorithm worked!\n')
	print(f'We were able to nicefy the diagram given in {input_path}')
	print('\n')

	if args.print_details_nicefication:

		print(f'Number of generators of the diagram: {number_of_generators}')
		print(f'Number of cycle of the algorithm: {number_iteration_algorithm}')
		print(f'Number of regions of the diagram: {H_diagram.number_of_regions}')
		print('\n')

	output_detail_nicefication = f'Number of generators of the diagram: {number_of_generators}\n'
	output_detail_nicefication = output_detail_nicefication + f'Number of regions of the diagram: {H_diagram.number_of_regions}\n'
	output_detail_nicefication = output_detail_nicefication + 'Number of cycle of the algorithm: %d \n' %number_iteration_algorithm
	output_detail_nicefication = output_detail_nicefication + '\n\n\n\n\n'


	# If we are dealing with a 4-ended tangle diagram and the flags are activated,
	# we compute the input for the PQM.m Mathematica Package
	if (tangle_diagram_flag) and (args.print_output_for_PQM or args.save_output_for_PQM):

		output_string_to_print_PQM, output_string_PQM = output_for_computing_invariant(H_diagram, number_border_points, alpha_arcs_sites, alexander_grading)

		if args.print_output_for_PQM:

			print("This is the string to copy and paste as PQM.m Mathematica Package input: \n")

			if args.user_experience:
				input('\nPress enter to continue...')

			print("\n")
			print("\n")

			print(output_string_to_print_PQM)


	if args.print_final_diagram:
		print(H_diagram)


	# We render the intermediate steps of the run. We always bind the string, so
	# that the output stage below cannot reach it unbound
	output_intermediate_steps = ''

	if args.save_intermediate_steps:
		output_intermediate_steps = saving_intermediate_steps(parameters_dict, intermediate_steps, number_iteration_algorithm)


	if args.save_on_file:

		output_path.parent.mkdir(parents=True, exist_ok=True)

		with output_path.open('w') as outputstream:

			if args.save_details_nicefication:
				outputstream.write(output_detail_nicefication)

			if (tangle_diagram_flag) and (args.save_output_for_PQM):
				outputstream.write(output_string_PQM)

			if args.save_final_diagram:
				outputstream.write('\nFINAL DIAGRAM\n')
				outputstream.write(H_diagram.__str__())
				outputstream.write('\n')

			if args.save_intermediate_steps:
				outputstream.write(output_intermediate_steps)

		print(f'Nicefied diagram written to {output_path}')

	return 0


if __name__ == "__main__":
	sys.exit(main())
