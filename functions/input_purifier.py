import string # Used to eliminate the whitespaces of the input

def list_of_list_input(input):
	output = []
	
	# First, we clean the input by all the whitespaces
	input = input.translate({ord(c): None for c in string.whitespace})

	# We take out the first '[' and the last ']]'
	input = input[1:-2]
	
	# We split in different strings with '],' as separator, obtaining a list [ '[1,2', .... , '[9,10' ]
	output_partial = input.split('],')

	# We finally append the right annidated lists to the output
	for annidate_list in output_partial:
		if annidate_list:
			output.append(list(map(int, annidate_list[1:].split(','))))
		else:
			# This case if sanity check mostly
			pass

	return output



def list_input(input):
	output = []
	
	# First, we clean the input by all the whitespaces
	input = input.translate({ord(c): None for c in string.whitespace})

	# We take out the first '[' and the last ']'
	input = input[1:-1]

	# We create the right output
	output = list(map(int, input.split(',')))
	
	return output



def string_input(input):
	
	# We clean the input by all the whitespaces
	input = input.translate({ord(c): None for c in string.whitespace})

	# We make all the character not capital
	output = input.lower()

	return output