import sys

def get_index_of_edge(region_input, edge):

	found_index_flag = False

	index_wanted = 0
	for start,end in zip(region_input, region_input[1:]+ [region_input[0]]):

		if [start, end] == edge:
			found_index_flag = True
			break

		index_wanted = index_wanted + 1 

	if not found_index_flag:
		sys.exit(f"Error: we didn't found the index of the edge {edge} in the region {region_input}")

	return (index_wanted % len(region_input))