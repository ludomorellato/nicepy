import sys

def compare_possible_diagrams(diagram, possible_diagrams, total_complexities, number_generators):

    # We now need to understand wich diagram is better
    # We cycle until we get a diagram with which we can proceed
    good_diagram_found = False

    while not good_diagram_found:

        # First, we understand what is the maximum decremenet that we can do on the
        # total complexity and we select only the keys for such value
        minimal_value_complexity = min(total_complexities.values())

        # We save all the diagrams that reduce at maximum the total complexity
        minimal_complexity_keys = [key for key in total_complexities.keys() if total_complexities[key] == minimal_value_complexity]

        # We remove the keys extracted from the total_complexities dictionary and their values
        for key in list(total_complexities.keys()).copy():
            if key in minimal_complexity_keys:
                del total_complexities[key]
        
        # We create a dictionary with the possible keys and values for the generators of such diagrams
        generators_min_complexity = dict()

        for (key, value) in number_generators.items():
            if key in minimal_complexity_keys:
                generators_min_complexity[key] = value

        
        # We cycle until we find a good diagram or until we finish to examine the diagrams in generators_min_complexity
        while (not good_diagram_found) and generators_min_complexity:
            
            # We choose between the keys in generators_min_complexity the ones that has 
            # the least number of generators
            minimal_generators = min(generators_min_complexity.values())

            # We save all the keys of diagrams that reduce at maximum the total complexity
            minimal_generators_keys = [key for key in generators_min_complexity.keys() if generators_min_complexity[key] == minimal_generators]


            # We create a sub-dictionary of possible_diagrams with the diagrams with keys in minimal_generators_keys
            possible_diagrams_min_generators = dict()

            for (key, value) in possible_diagrams.items():
                if key in minimal_generators_keys:
                    possible_diagrams_min_generators[key] = value


            # We remove the keys extracted from the total_complexities dictionary and their values
            for key in list(generators_min_complexity.keys()).copy():
                if key in minimal_generators_keys:
                    del generators_min_complexity[key]

            
            # We need now to check that indeed the complexity of maximum distance decreased 
            # in one of the diagrams in possible_diagrams_min_generators

            # We find the diagram with the minimal distance complexity among the among the ones in possible_diagrams_min_generators
            better_diagram_temp = False

            for key in possible_diagrams_min_generators:

                if not better_diagram_temp:

                    better_diagram_temp = possible_diagrams_min_generators[key]
                
                else:
                    
                    keep_new_diagram = is_new_diagram_better(possible_diagrams_min_generators[key], better_diagram_temp)

                    if keep_new_diagram:

                        better_diagram_temp = possible_diagrams_min_generators[key]

                    else:

                        pass

            
            # We now check if we did get a better diagram with respect to the old one
            good_diagram_found = is_new_diagram_better(better_diagram_temp, diagram)



    return better_diagram_temp






















def is_new_diagram_better(new_diagram, old_diagram):

    distance_new_diagram = new_diagram.distance_diagram

    # We check if new_diagram is nice
    if distance_new_diagram == 0:
        return True

    distance_complexity_new_diagram = new_diagram.distance_complexities[distance_new_diagram]

    distance_old_diagram = old_diagram.distance_diagram
    distance_complexity_old_diagram = old_diagram.distance_complexities[distance_old_diagram]


    if distance_new_diagram < distance_old_diagram:

        # The distance decreased, new_diagram is better
        return True

    elif distance_new_diagram > distance_old_diagram:

        # The distance increased, the diagram is worst
        return False

    else:

        # The distances are the same, we need to study the distance complexity of maximum distance

        # We first check the total badness
        if distance_complexity_new_diagram[0] < distance_complexity_old_diagram[0]:

            return True
        
        elif distance_complexity_new_diagram[0] > distance_complexity_old_diagram[0]:

            # The distance complexity increased, the diagram is worst
            pass
            
        else:

            # The total badness is the same, we need to check the rest of the tuples
            
            minimal_length_temp = min(len(distance_complexity_new_diagram), len(distance_complexity_old_diagram))

            # We check the two tuples
            for index in range(1, minimal_length_temp):

                if distance_complexity_new_diagram[index][0] < distance_complexity_old_diagram[index][0]:

                    # The distance complexity decreased, the diagram is better
                    return True
                
                elif distance_complexity_new_diagram[index][0] > distance_complexity_old_diagram[index][0]:

                    # The distance complexity increased, the diagram is worst
                    return False

                else:

                    # This term is equal, we proceed
                    pass
            
            # We didn't found an inequality between the two tuples
            # We check if also the length is the same (and in such case, old and new diagram are the same), 
            # if they are not we throw an error (this case should not ever happen)
           
            if len(distance_complexity_new_diagram) == len(distance_complexity_old_diagram):

                # The two complexities are the same, the new one is worst
                return False

            else:

                # The two complexities are different, we should have found a difference at some point
                # We throw an error

                sys.exit(f"We compared two different complexities, the old one: {distance_complexity_old_diagram} and the new one: {distance_complexity_new_diagram} and we didn't find them to be different as we should had")