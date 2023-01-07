def find_best_final_diagram(possible_final_diagrams):

    minimal_number_generators = False
    index_minimal_number_generators = False
    
    # We iterate between the possible number of generators, finding the minimum one
    for index in possible_final_diagrams:

        generators_temp = possible_final_diagrams[index]['number_of_generators']

        # Base case, we assign the minimal number of generator for the first time
        if not minimal_number_generators:
            
            minimal_number_generators = generators_temp
            index_minimal_number_generators = index

        # If we found a new diagram with less generators, we change the values
        elif generators_temp < minimal_number_generators:

            minimal_number_generators = generators_temp
            index_minimal_number_generators = index

        # Otherwise, we just pass
        else: 
            
            pass

    
    # We return the best diagram
    return possible_final_diagrams[index_minimal_number_generators]