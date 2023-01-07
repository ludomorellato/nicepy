import math

def compute_distance_complexities_diagram(diagram):
    complexities = dict()
    not_ordered_complexities = dict(sorted(diagram.distance_complexities.items()))

    # We want to also save the total complexity
    total_complexity = 0

    for distance in not_ordered_complexities:

        complexities[distance] = [(-not_ordered_complexities[distance][0].badness, not_ordered_complexities[distance][0])]
        sum_badnesses = not_ordered_complexities[distance][0].badness

        for bad_region in not_ordered_complexities[distance][1:]:
            
            # We partially compute the sum of the badnesses, we'll add it in the end to the list
            sum_badnesses = sum_badnesses + bad_region.badness

            # We put  the tuple (-badness, region) in the right spot
            if complexities[distance][0][0] > -bad_region.badness:
                complexities[distance] = [(-bad_region.badness, bad_region)] + complexities[distance]
            else:

                # We create a flag to know if we have placed the new region somewhere
                flag_region_placed = False

                # We try to put the region somewhere
                for index in range(len(complexities[distance]) - 1):
                    if (complexities[distance][index][0] <= -bad_region.badness) and (complexities[distance][index + 1][0] > -bad_region.badness):
                        complexities[distance] = complexities[distance][:index +1] + [(-bad_region.badness, bad_region)] + complexities[distance][index +1:]
                        flag_region_placed = True
                        break

                if not flag_region_placed:
                    # The region was not placed, therefore it has to be the last one on the list
                    complexities[distance] = complexities[distance] + [(-bad_region.badness, bad_region)]        
       
        # We add the sum in front of the list
        complexities[distance] = [sum_badnesses] + complexities[distance]

        # We add the total badness of distance to the total complexity
        # Notice that we multiply the sum_badnesses by 3 elevate at the distance of that badnesses
        total_complexity = total_complexity + sum_badnesses*(3**distance)
    
    # Notice that if we don't have any bad region of positive distance, we are returning 
    # an empty dictionary
    return (complexities, total_complexity)