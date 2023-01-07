import sys

def heegaard_diagram_for_rational_tangle(sign, p, q, label_to_skip):

    # In this function, we construct the Heegaard diagram for a rational 
    # tangle, given by its canonical form as ± p/q

    difference = p - q

    common_border_region = dict()

    if p == 1 and q == 1:
        
        # In this base case, we construct the diagram by hands
        if sign == '+':

            # BORDER REGIONS
            # We manually construct the border regions of the diagram (that are all the regions of the diagram)

            bottom_left_in = [4, 10+label_to_skip, 11+label_to_skip, 7, 8, 12+label_to_skip, 9+label_to_skip, 3]
            bottom_left_out = [3, 9+label_to_skip, 10+label_to_skip, 4]

            top_right_out = [7, 11+label_to_skip, 12+label_to_skip, 8]
            top_right_in = [8, 12+label_to_skip, 9+label_to_skip, 3, 4, 10+label_to_skip, 11+label_to_skip, 7]
            common_border_region['bottom_left_in'] = 'top_right_in'
            common_border_region['top_right_in'] = 'bottom_left_in'

            bottom_right_in = [6, 11+label_to_skip, 10+label_to_skip, 5]
            bottom_right_out = [5, 10+label_to_skip, 9+label_to_skip, 2, 1, 12+label_to_skip, 11+label_to_skip, 6]

            top_left_in = [2, 9+label_to_skip, 12+label_to_skip, 1]
            top_left_out = [1, 12+label_to_skip, 11+label_to_skip, 6, 5, 10+label_to_skip, 9+label_to_skip, 2]
            common_border_region['bottom_right_out'] = 'top_left_out'
            common_border_region['top_left_out'] = 'bottom_right_out'
            

        else:

            # BORDER REGIONS
            # We manually construct the border regions of the diagram (that are all the regions of the diagram)

            bottom_left_in = [4, 10+label_to_skip, 9+label_to_skip, 3]
            bottom_left_out = [3, 9+label_to_skip, 12+label_to_skip, 8, 7, 11+label_to_skip, 10+label_to_skip, 4]

            top_right_in = [8, 12+label_to_skip, 11+label_to_skip, 7]
            top_right_out = [7, 11+label_to_skip, 10+label_to_skip, 4, 3, 9+label_to_skip, 12+label_to_skip, 8]
            common_border_region['bottom_left_out'] = 'top_right_out'
            common_border_region['top_right_out'] = 'bottom_left_out'

            bottom_right_in = [6, 11+label_to_skip, 12+label_to_skip, 1, 2, 9+label_to_skip, 10+label_to_skip, 5]
            bottom_right_out = [5, 10+label_to_skip, 11+label_to_skip, 6]

            top_left_out = [1, 12+label_to_skip, 9+label_to_skip, 2]
            top_left_in = [2, 9+label_to_skip, 10+label_to_skip, 5, 6, 11+label_to_skip, 12+label_to_skip, 1]
            common_border_region['bottom_right_in'] = 'top_left_in'
            common_border_region['top_left_in'] = 'bottom_right_in'


        # We save the border regions in a dictionary, they will be used in the case of gluing
        # We also save the data of being on the inside (0) or on the outside (1)
        border_regions = dict()

        border_regions['top_left_in'] = [top_left_in, 0]
        border_regions['top_left_out'] = [top_left_out, 1]
        border_regions['bottom_left_in'] = [bottom_left_in, 0]
        border_regions['bottom_left_out'] = [bottom_left_out, 1]
        border_regions['bottom_right_in'] = [bottom_right_in, 0]
        border_regions['bottom_right_out'] = [bottom_right_out, 1]
        border_regions['top_right_in'] = [top_right_in, 0]
        border_regions['top_right_out'] = [top_right_out, 1]
        border_regions['common_border_region'] = common_border_region



        # We give the output as a dictionary
        output = dict()

        output['border_regions'] = border_regions
        output['regions_input'] = []
        output['label_to_skip'] = 2*p + 2*q + label_to_skip


    else:

        # We are in a non trivial case, in which at least one between p and q is greater or equal to 2

            
        if difference == 0:
            sys.exit('Error: p is equal to q and they are not 1')

        if sign == '+':

            # In this case, we link the intersection points in a way that the 
            # internal lines have positive sloper





            # BORDER REGIONS
            # First, we manually construct the border regions of the diagram

            bottom_left_in = [4, q+1+8+label_to_skip, 2*q+p+8+label_to_skip+difference, 2*q+p+8+label_to_skip+difference + 1, q+8+label_to_skip, 3]
            bottom_left_out = [3, q+8+label_to_skip, q+8+label_to_skip + 1, 4]

            top_right_in = [8, 2*q+p+8+label_to_skip + 1, q+8+label_to_skip+difference, q+8+label_to_skip+difference + 1, 2*q+p+8+label_to_skip, 7]
            top_right_out = [7, 2*q+p+8+label_to_skip, 2*q+p+8+label_to_skip + 1, 8]

            bottom_right_in = [6, q+p+8+label_to_skip + 1, q+p+8+label_to_skip, 5]

            top_left_in = [2, 8+label_to_skip+1, 2*q+2*p+8+label_to_skip, 1]
            top_left_out = [1, 2*q+2*p+8+label_to_skip, q+p+1-difference+8+label_to_skip, q+p+1-difference+8+label_to_skip - 1, 8+label_to_skip+1, 2]

            if difference > 0:
                bottom_right_out = [5, q+p+8+label_to_skip, 2*q+2*p+1-difference+8+label_to_skip, 2*q+2*p+1-difference+8+label_to_skip - 1, q+p+1+8+label_to_skip, 6]

            else:
                bottom_right_out = [5, q+p+8+label_to_skip, 1-difference+8+label_to_skip, 1-difference+8+label_to_skip - 1, q+p+1+8+label_to_skip, 6]



            # We save the border regions in a dictionary, they will be used in the case of gluing
            # We also save the data of being on the inside (0) or on the outside (1)
            border_regions = dict()

            border_regions['top_left_in'] = [top_left_in, 0]
            border_regions['top_left_out'] = [top_left_out, 1]
            border_regions['bottom_left_in'] = [bottom_left_in, 0]
            border_regions['bottom_left_out'] = [bottom_left_out, 1]
            border_regions['bottom_right_in'] = [bottom_right_in, 0]
            border_regions['bottom_right_out'] = [bottom_right_out, 1]
            border_regions['top_right_in'] = [top_right_in, 0]
            border_regions['top_right_out'] = [top_right_out, 1]
            border_regions['common_border_region'] = dict()




            # INTERNAL REGIONS
            
            # We construct now the internal regions without border
            internal_regions = []

            upper_temp = 2*p + 2*q + 8+label_to_skip
            lower_temp = 8+label_to_skip+1

            min_p_q = min([p,q])


            # We start by the top-left corner, we construct the regions from the top-left border regions
            # to the bottom-left border region
            # There are exaclty min(p,q)-1 regions here
            for i in range(1, min_p_q):
                
                # We add the square region
                internal_regions.append([lower_temp, lower_temp + 1, upper_temp - 1, upper_temp])

                # We modify the counters
                upper_temp = upper_temp - 1
                lower_temp = lower_temp + 1

            

            # We reached the bottom-left border region in the middle, we skip it
            upper_temp = upper_temp - 1
            lower_temp = lower_temp + 1



            # We construct the regions between the the bottom-left border region and the top-right border region
            # There are exaclty abs(difference)-1 regions here
            for i in range(1, abs(difference)):
                
                # We add the square region
                internal_regions.append([lower_temp, lower_temp + 1, upper_temp - 1, upper_temp])

                # We modify the counters
                upper_temp = upper_temp - 1
                lower_temp = lower_temp + 1

            

            # We reached the top-right border region in the middle, we skip it
            upper_temp = upper_temp - 1
            lower_temp = lower_temp + 1


            # We construct the regions up to the bottom-right border region
            # There are exaclty min(p,q)-1 regions here
            for i in range(1, min_p_q):
                
                # We add the square region
                internal_regions.append([lower_temp, lower_temp + 1, upper_temp - 1, upper_temp])

                # We modify the counters
                upper_temp = upper_temp - 1
                lower_temp = lower_temp + 1








            
            # EXTERNAL REGIONS
            
            # We construct now the external regions without border
            external_regions = []

            # We create a list in the right order for the points on the left side (there is the change from 8+label_to_skip+1 to 2*p+2*q+8+label_to_skip to deal with)
            top_temp_list = list(range(q+8+label_to_skip, 8+label_to_skip, -1)) + list(range(2*p+2*q+8+label_to_skip, 2*q+p+8+label_to_skip, -1))
            top_temp_index = 0

            bottom_temp = q + 8+label_to_skip+1

            min_p_q = min([p,q])


            # We start by the top-left corner, we construct the regions from the top-left border regions
            # to the bottom-left border region
            # There are exaclty min(p,q)-1 regions here
            for i in range(1, min_p_q):
                
                # We add the square region
                external_regions.append([bottom_temp + 1, bottom_temp, top_temp_list[top_temp_index], top_temp_list[top_temp_index] - 1])

                # We modify the counters
                top_temp_index = top_temp_index + 1
                bottom_temp = bottom_temp + 1

            

            # We reached the bottom-left border region in the middle, we skip it
            top_temp_index = top_temp_index + 1
            bottom_temp = bottom_temp + 1



            # We construct the regions between the the bottom-left border region and the top-right border region
            # There are exaclty abs(difference)-1 regions here
            for i in range(1, abs(difference)):
                
                # We add the square region
                external_regions.append([bottom_temp + 1, bottom_temp, top_temp_list[top_temp_index], top_temp_list[top_temp_index] - 1])

                # We modify the counters
                top_temp_index = top_temp_index + 1
                bottom_temp = bottom_temp + 1

            

            # We reached the top-right border region in the middle, we skip it
            top_temp_index = top_temp_index + 1
            bottom_temp = bottom_temp + 1


            # We construct the regions up to the bottom-right border region
            # There are exaclty min(p,q)-1 regions here
            for i in range(1, min_p_q):
                
                # We add the square region
                external_regions.append([bottom_temp + 1, bottom_temp, top_temp_list[top_temp_index], top_temp_list[top_temp_index] - 1])

                # We modify the counters
                top_temp_index = top_temp_index + 1
                bottom_temp = bottom_temp + 1



        if sign == '-':

            # In this case, we link the intersection points in a way that the 
            # internal lines have negative sloper





            # BORDER REGIONS
            # First, we manually construct the border regions of the diagram

            bottom_left_out = [3, q+8+label_to_skip, 2*q+p+8+label_to_skip+difference + 1, 2*q+p+8+label_to_skip+difference, q+8+label_to_skip + 1, 4]
            bottom_left_in = [4, q+8+label_to_skip + 1, q+8+label_to_skip, 3]

            top_right_out = [7, 2*q+p+8+label_to_skip, q+8+label_to_skip+difference + 1, q+8+label_to_skip+difference, 2*q+p+8+label_to_skip + 1, 8]
            top_right_in = [8, 2*q+p+8+label_to_skip + 1, 2*q+p+8+label_to_skip, 7]

            bottom_right_out = [5, q+p+8+label_to_skip, q+p+8+label_to_skip + 1, 6]

            top_left_out = [1, 2*q+2*p+8+label_to_skip, 8+label_to_skip+1, 2]
            top_left_in = [2, 8+label_to_skip+1, q+p+1-difference+8+label_to_skip - 1, q+p+1-difference+8+label_to_skip, 2*q+2*p+8+label_to_skip, 1]

            if difference > 0:
                bottom_right_in = [6, q+p+8+label_to_skip + 1, 2*q+2*p+1-difference+8+label_to_skip - 1, 2*q+2*p+1-difference+8+label_to_skip, q+p+8+label_to_skip, 5]

            else:
                bottom_right_in = [6, q+p+8+label_to_skip + 1, 1-difference+8+label_to_skip - 1, 1-difference+8+label_to_skip, q+p+8+label_to_skip, 5]



            # We save the border regions in a dictionary, they will be used in the case of gluing
            border_regions = dict()

            border_regions['top_left_in'] = [top_left_in, 0]
            border_regions['top_left_out'] = [top_left_out, 1]
            border_regions['bottom_left_in'] = [bottom_left_in, 0]
            border_regions['bottom_left_out'] = [bottom_left_out, 1]
            border_regions['bottom_right_in'] = [bottom_right_in, 0]
            border_regions['bottom_right_out'] = [bottom_right_out, 1]
            border_regions['top_right_in'] = [top_right_in, 0]
            border_regions['top_right_out'] = [top_right_out, 1]
            border_regions['common_border_region'] = dict()












            # INTERNAL REGIONS
            
            # We construct now the internal regions without border
            internal_regions = []

            # We create a list in the right order for the points on the left side (there is the change from 8+label_to_skip+1 to 2*p+2*q+8+label_to_skip to deal with)
            top_temp_list = list(range(q+8+label_to_skip, 8+label_to_skip, -1)) + list(range(2*p+2*q+8+label_to_skip, 2*q+p+8+label_to_skip, -1))
            top_temp_index = 0

            bottom_temp = q + 8+label_to_skip+1

            min_p_q = min([p,q])


            # We start by the top-left corner, we construct the regions from the top-left border regions
            # to the bottom-left border region
            # There are exaclty min(p,q)-1 regions here
            for i in range(1, min_p_q):
                
                # We add the square region
                internal_regions.append([bottom_temp, bottom_temp + 1, top_temp_list[top_temp_index] - 1, top_temp_list[top_temp_index]])

                # We modify the counters
                top_temp_index = top_temp_index + 1
                bottom_temp = bottom_temp + 1

            

            # We reached the bottom-left border region in the middle, we skip it
            top_temp_index = top_temp_index + 1
            bottom_temp = bottom_temp + 1



            # We construct the regions between the the bottom-left border region and the top-right border region
            # There are exaclty abs(difference)-1 regions here
            for i in range(1, abs(difference)):
                
                # We add the square region
                internal_regions.append([bottom_temp, bottom_temp + 1, top_temp_list[top_temp_index] - 1, top_temp_list[top_temp_index]])

                # We modify the counters
                top_temp_index = top_temp_index + 1
                bottom_temp = bottom_temp + 1

            

            # We reached the top-right border region in the middle, we skip it
            top_temp_index = top_temp_index + 1
            bottom_temp = bottom_temp + 1


            # We construct the regions up to the bottom-right border region
            # There are exaclty min(p,q)-1 regions here
            for i in range(1, min_p_q):
                
                # We add the square region
                internal_regions.append([bottom_temp, bottom_temp + 1, top_temp_list[top_temp_index] - 1, top_temp_list[top_temp_index]])

                # We modify the counters
                top_temp_index = top_temp_index + 1
                bottom_temp = bottom_temp + 1








            # EXTERNAL REGIONS
            
            # We construct now the external regions without border
            external_regions = []

            upper_temp = 2*p + 2*q + 8+label_to_skip
            lower_temp = 8+label_to_skip+1

            min_p_q = min([p,q])


            # We start by the top-left corner, we construct the regions from the top-left border regions
            # to the bottom-left border region
            # There are exaclty min(p,q)-1 regions here
            for i in range(1, min_p_q):
                
                # We add the square region
                external_regions.append([lower_temp + 1, lower_temp, upper_temp, upper_temp - 1])

                # We modify the counters
                upper_temp = upper_temp - 1
                lower_temp = lower_temp + 1

            

            # We reached the bottom-left border region in the middle, we skip it
            upper_temp = upper_temp - 1
            lower_temp = lower_temp + 1



            # We construct the regions between the the bottom-left border region and the top-right border region
            # There are exaclty abs(difference)-1 regions here
            for i in range(1, abs(difference)):
                
                # We add the square region
                external_regions.append([lower_temp + 1, lower_temp, upper_temp, upper_temp - 1])

                # We modify the counters
                upper_temp = upper_temp - 1
                lower_temp = lower_temp + 1

            

            # We reached the top-right border region in the middle, we skip it
            upper_temp = upper_temp - 1
            lower_temp = lower_temp + 1


            # We construct the regions up to the bottom-right border region
            # There are exaclty min(p,q)-1 regions here
            for i in range(1, min_p_q):
                
                # We add the square region
                external_regions.append([lower_temp + 1, lower_temp, upper_temp, upper_temp - 1])

                # We modify the counters
                upper_temp = upper_temp - 1
                lower_temp = lower_temp + 1








        # We give the output as a dictionary
        output = dict()

        output['border_regions'] = border_regions
        output['regions_input'] = internal_regions + external_regions
        output['label_to_skip'] = 2*p + 2*q + label_to_skip



    return output