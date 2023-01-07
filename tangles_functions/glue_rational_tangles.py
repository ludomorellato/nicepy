import sys

from functions.get_index_of_edge import get_index_of_edge


def glue_rational_tangles(diagrams_tangles, gluing_instructions, tangles_input):

    # Recall that gluing are given as
    #       [label tangle 1, end to glue of tangle 1, label tangle 2, end to glue of tangle 2]
    # where
    #       1 = top left end
    #       2 = bottom left end
    #       3 = bottom right end
    #       4 = top right end
    
    
    new_regions_created = []
    alert_possible_link = False

    for gluing in gluing_instructions:
        
        label_1 = gluing[0]
        label_2 = gluing[2]
        end_1 = gluing[1]
        end_2 = gluing[3]



        # First of all, we check that we are not constructing a link inside our tangle.
        # Let be p_1, q_1 the parameters of the first tangle and p_2, q_2 the ones of the second.
        # We claim that a link appears if and only if p, p' are odd and q, q' are even.
        # We therefore check this case.

        p_1 = tangles_input[label_1 - 1][1]
        q_1 = tangles_input[label_1 - 1][2]
        p_2 = tangles_input[label_2 - 1][1]
        q_2 = tangles_input[label_2 - 1][2]

        p_both_odd = (p_1 % 2 == 1) and (p_2 % 2 == 1)
        q_both_even = (q_1 % 2 == 0) and (q_2 % 2 == 0)

        if p_both_odd and q_both_even and not alert_possible_link:
            s = f'A link is probably going to be generated and the program will fail. \nThe problem is the gluing between the tangle number {label_1} and the tangle number {label_2}.'
            s = s + '\nIf you still want to procede with the program, press Enter'
            input(s)
            alert_possible_link = True
        
        
        
        
        # We need to understand how to link the alpha arcs. We do this manually
        # It is not very clear to me why it works like that, but seems to be the case
        border_point_1_a = end_1*2 - 1
        border_point_1_b = end_1*2

        border_point_2_a = end_2*2       
        border_point_2_b = end_2*2 - 1

        '''
        if end_1 == 1:

            border_point_1_a = 1
            border_point_2_a = 2

            if end_2 == 1:
                
                border_point_1_b = 2            
                border_point_2_b = 1

            elif end_2 == 2:

                border_point_1_b = 4
                border_point_2_b = 3
            
            elif end_2 == 3:

                border_point_1_b = 6
                border_point_2_b = 5

            elif end_2 == 4:

                border_point_1_b = 8
                border_point_2_b = 7

        elif end_1 == 2:

            border_point_1_a = 3
            border_point_1_b = 4

            if end_2 == 1:
                
                border_point_1_b = 2            
                border_point_2_b = 1

            elif end_2 == 2:

                border_point_1_b = 4
                border_point_2_b = 3
            
            elif end_2 == 3:

                border_point_1_b = 6
                border_point_2_b = 5

            elif end_2 == 4:

                border_point_1_b = 8
                border_point_2_b = 7
            '''
        
        
        
        # We identify the regions to glue together
        regions_to_glue = identify_regions_to_glue(end_1, end_2, label_1, label_2, diagrams_tangles)

        region_in_1 = regions_to_glue['region_in_1']
        region_out_1 = regions_to_glue['region_out_1']
        region_in_2 = regions_to_glue['region_in_2']
        region_out_2 = regions_to_glue['region_out_2']
        more_than_one_border_component = regions_to_glue['more_than_one_border_component']




        '''
        # We now compute the indicies of the border points in the regions

        # For the internal region in tangle 1
        border_point_1_a_in_index = get_index_of_edge(region_in_1, border_point_1_a) 
        border_point_1_b_in_index = get_index_of_edge(region_in_1, border_point_1_b) 

        # For the internal region in tangle 2
        border_point_2_a_in_index = get_index_of_edge(region_in_2, border_point_2_a)        
        border_point_2_b_in_index = get_index_of_edge(region_in_2, border_point_2_b)

        # For the external region in tangle 1
        border_point_1_a_out_index = get_index_of_edge(region_out_1, border_point_1_a) 
        border_point_1_b_out_index = get_index_of_edge(region_out_1, border_point_1_b) 

        # For the external region in tangle 2
        border_point_2_a_out_index = get_index_of_edge(region_out_2, border_point_2_a)        
        border_point_2_b_out_index = get_index_of_edge(region_out_2, border_point_2_b)
        






        # We can finally merge the regions

        new_region_in = []

        if border_point_1_a_in_index < border_point_1_b_in_index:

            if border_point_2_a_in_index < border_point_2_b_in_index:
                
                new_region_in = region_in_1[0 : border_point_1_a_in_index + 1] + region_in_2 + region_in_1[border_point_1_b_in_index: ]
            
            else:
                
                new_region_in = region_in_1[0 : border_point_1_a_in_index + 1] + region_in_2[border_point_2_a_in_index: ] + region_in_2[ : border_point_2_b_in_index + 1] + region_in_1[border_point_1_b_in_index: ]
            

        else:

            if border_point_2_a_in_index < border_point_2_b_in_index:

                new_region_in = []

            else:

                new_region_in = []
        '''


        # We can merge the regions

        new_region_in = region_in_1[2:-1] + region_in_2[1:-1] + [region_in_1[1]]
        new_region_out = region_out_1[2:-1] + region_out_2[1:-1] + [region_out_1[1]]


        # We check if we have some regions with more than one border component
        if more_than_one_border_component:
            
            label_tangle = list(more_than_one_border_component.keys())[0]

            in_or_out = list(more_than_one_border_component[label_tangle].keys())[0]
            border_region_to_substitute = more_than_one_border_component[label_tangle][in_or_out]

            if in_or_out == 'other_region_in':

                # We have to re-order new_region_in, so that it has the border points
                # as beginning and end

                for index_border_point in range(len(new_region_in)):
                    
                    if new_region_in[index_border_point] < 9:

                        break

                # We have the index of the first border point, the second one is the next one
                # We write the new region in in the right order
                new_region_in = new_region_in[index_border_point + 1: ] + new_region_in[: index_border_point + 1]


                # Then, we save new_region_in as border region in the tangle label_tangle
                diagrams_tangles[label_tangle][1][border_region_to_substitute] = [new_region_in, 0]

                # And we append the outer region to the list of new regions
                new_regions_created.append(new_region_out)

                # We remove the data of the link between the two border region in the dictionary of the tangle label_tangle
                del diagrams_tangles[label_tangle][1]['common_border_region'][diagrams_tangles[label_tangle][1]['common_border_region'][border_region_to_substitute]]
                del diagrams_tangles[label_tangle][1]['common_border_region'][border_region_to_substitute]


            elif in_or_out == 'other_region_out':
                
                # We have to re-order new_region_in, so that it has the border points
                # as beginning and end

                for index_border_point in range(len(new_region_out)):
                    
                    if new_region_out[index_border_point] < 9:

                        break

                # We have the index of the first border point, the second one is the next one
                # We write the new region in in the right order
                new_region_out = new_region_out[index_border_point + 1: ] + new_region_out[: index_border_point + 1]


                # Then, we save new_region_out as border region in the tangle label_tangle
                diagrams_tangles[label_tangle][1][border_region_to_substitute] = [new_region_out, 1]

                # And we append the inner region to the list of new regions
                new_regions_created.append(new_region_in)


                # We remove the data of the link between the two border region in the dictionary of the tangle label_tangle
                del diagrams_tangles[label_tangle][1]['common_border_region'][diagrams_tangles[label_tangle][1]['common_border_region'][border_region_to_substitute]]
                del diagrams_tangles[label_tangle][1]['common_border_region'][border_region_to_substitute]


            else:

                # Sanity check, we shouldn't come here
                sys.exit('Problem: gluing of tangles with regions with more than one border component')

        
        else:

            # We don't have regions with more than one border component between the ones
            # that we glued together

            # We append these new region in the list of the new regions
            new_regions_created.append(new_region_in)
            new_regions_created.append(new_region_out)



    '''
    # We can now put all the regions together
    # While we do that, we save also the datas for the multiplicity zero regions

    glued_tangle_input = new_regions_created
    multiplicity_zero_regions_temp = []

    for index in diagrams_tangles.keys():

        tangle = diagrams_tangles[index]

        glued_tangle_input = glued_tangle_input + tangle[0]

        for key in tangle[1].keys():
            glued_tangle_input.append(tangle[1][key][0])
            multiplicity_zero_regions_temp.append([glued_tangle_input[-1], len(glued_tangle_input), tangle[1][key][1]])
    '''



    # We can now put all the regions together
    # While we do that, we save also the datas for the multiplicity zero regions

    # We save in glued_tangle_input all the new regions created by the gluing
    glued_tangle_input = new_regions_created

    multiplicity_zero_regions_temp_inside = []
    multiplicity_zero_regions_temp_outside = []

    for index in diagrams_tangles.keys():

        # We take the tangle of index 'index'
        tangle = diagrams_tangles[index]

        # We add to glued_tangle_input the list of regions without border of tangle 
        glued_tangle_input = glued_tangle_input + tangle[0]

        for key in tangle[1].keys():

            if key == 'common_border_region':

                # Here we don't have regions to add
                pass
            
            else:

                # We add to glued_tangle_input the list of border regions regions of tangle
                glued_tangle_input.append(tangle[1][key][0])
                
                if tangle[1][key][1] == 0:

                    # We keep track of the multiplicity zero regions (and if they are inside or outside)
                    multiplicity_zero_regions_temp_inside.append([len(glued_tangle_input), 0])

                else:

                    # We keep track of the multiplicity zero regions (and if they are inside or outside)
                    multiplicity_zero_regions_temp_outside.append([len(glued_tangle_input), 1])





    
    '''
    # We now decide where to actually put the multiplicity zero basepoints
    
    multiplicity_zero_regions = []

    # We set two flags to False, they are going to be True when we find a suitable region
    inside_flag = False
    outside_flag = False

    for candidate in multiplicity_zero_regions_temp:

        if (not inside_flag) and (candidate[2] == 0) and (len(candidate[0]) > 3):
            multiplicity_zero_regions.append([candidate[1], candidate[2]])
            inside_flag = True

        if (not outside_flag) and (candidate[2] == 1) and (len(candidate[0]) > 3):
            multiplicity_zero_regions.append([candidate[1], candidate[2]])
            outside_flag = True

        if inside_flag and outside_flag:
            break
    '''



    # We now compute all the possibilities regarding where to place the basepoints
    # and we save them inside a list
    possible_multiplicity_zero_regions = []

    for internal_region in multiplicity_zero_regions_temp_inside:

        for external_region in multiplicity_zero_regions_temp_outside:

            possible_multiplicity_zero_regions.append([internal_region, external_region])





    output = dict()
    output['glued_tangle_input'] = glued_tangle_input
    output['possible_multiplicity_zero_regions'] = possible_multiplicity_zero_regions


    return output













def identify_regions_to_glue(end_1, end_2, label_1, label_2, diagrams_tangles):

    # We create a diagram to keep trakc of the possibility of border regions 
    # that touch more than one border (this appens if we started from a 1/1 rational tangle)
    more_than_one_border_component = dict()

    # We identify the regions for the first diagram
    if end_1 == 1:

        region_in_1 = diagrams_tangles[label_1][1]['top_left_in'][0]
        region_out_1 = diagrams_tangles[label_1][1]['top_left_out'][0]

        # We eliminate these regions from the dictionary of border regions
        del diagrams_tangles[label_1][1]['top_left_in']
        del diagrams_tangles[label_1][1]['top_left_out']

        # We check if they are also border region on another angle 
        # (this appens if we started from a 1/1 rational tangle)
        another_border_region = check_another_border_region('top_left_in', 'top_left_out', diagrams_tangles, label_1)

        if another_border_region:

            more_than_one_border_component[label_1] = another_border_region



    elif end_1 == 2:

        region_in_1 = diagrams_tangles[label_1][1]['bottom_left_in'][0]
        region_out_1 = diagrams_tangles[label_1][1]['bottom_left_out'][0]

        # We eliminate these regions from the dictionary of border regions
        del diagrams_tangles[label_1][1]['bottom_left_in']
        del diagrams_tangles[label_1][1]['bottom_left_out']

        # We check if they are also border region on another angle 
        # (this appens if we started from a 1/1 rational tangle)
        another_border_region = check_another_border_region('bottom_left_in', 'bottom_left_out', diagrams_tangles, label_1)

        if another_border_region:

            more_than_one_border_component[label_1] = another_border_region


    elif end_1 == 3:

        region_in_1 = diagrams_tangles[label_1][1]['bottom_right_in'][0]
        region_out_1 = diagrams_tangles[label_1][1]['bottom_right_out'][0]

        # We eliminate these regions from the dictionary of border regions
        del diagrams_tangles[label_1][1]['bottom_right_in']
        del diagrams_tangles[label_1][1]['bottom_right_out']

        # We check if they are also border region on another angle 
        # (this appens if we started from a 1/1 rational tangle)
        another_border_region = check_another_border_region('bottom_right_in', 'bottom_right_out', diagrams_tangles, label_1)

        if another_border_region:

            more_than_one_border_component[label_1] = another_border_region


    elif end_1 == 4:

        region_in_1 = diagrams_tangles[label_1][1]['top_right_in'][0]
        region_out_1 = diagrams_tangles[label_1][1]['top_right_out'][0]

        # We eliminate these regions from the dictionary of border regions
        del diagrams_tangles[label_1][1]['top_right_in']
        del diagrams_tangles[label_1][1]['top_right_out']

        # We check if they are also border region on another angle 
        # (this appens if we started from a 1/1 rational tangle)
        another_border_region = check_another_border_region('top_right_in', 'top_right_out', diagrams_tangles, label_1)

        if another_border_region:

            more_than_one_border_component[label_1] = another_border_region



    # We identify the regions for the second diagram
    if end_2 == 1:

        region_in_2 = diagrams_tangles[label_2][1]['top_left_in'][0]
        region_out_2 = diagrams_tangles[label_2][1]['top_left_out'][0]

        # We eliminate these regions from the dictionary of border regions
        del diagrams_tangles[label_2][1]['top_left_in']
        del diagrams_tangles[label_2][1]['top_left_out']

        # We check if they are also border region on another angle 
        # (this appens if we started from a 1/1 rational tangle)
        another_border_region = check_another_border_region('top_left_in', 'top_left_out', diagrams_tangles, label_2)

        if another_border_region:

            more_than_one_border_component[label_2] = another_border_region

    elif end_2 == 2:

        region_in_2 = diagrams_tangles[label_2][1]['bottom_left_in'][0]
        region_out_2 = diagrams_tangles[label_2][1]['bottom_left_out'][0]

        # We eliminate these regions from the dictionary of border regions
        del diagrams_tangles[label_2][1]['bottom_left_in']
        del diagrams_tangles[label_2][1]['bottom_left_out']

        # We check if they are also border region on another angle 
        # (this appens if we started from a 1/1 rational tangle)
        another_border_region = check_another_border_region('bottom_left_in', 'bottom_left_out', diagrams_tangles, label_2)

        if another_border_region:

            more_than_one_border_component[label_2] = another_border_region


    elif end_2 == 3:

        region_in_2 = diagrams_tangles[label_2][1]['bottom_right_in'][0]
        region_out_2 = diagrams_tangles[label_2][1]['bottom_right_out'][0]

        # We eliminate these regions from the dictionary of border regions
        del diagrams_tangles[label_2][1]['bottom_right_in']
        del diagrams_tangles[label_2][1]['bottom_right_out']

        # We check if they are also border region on another angle 
        # (this appens if we started from a 1/1 rational tangle)
        another_border_region = check_another_border_region('bottom_right_in', 'bottom_right_out', diagrams_tangles, label_2)

        if another_border_region:

            more_than_one_border_component[label_2] = another_border_region


    elif end_2 == 4:

        region_in_2 = diagrams_tangles[label_2][1]['top_right_in'][0]
        region_out_2 = diagrams_tangles[label_2][1]['top_right_out'][0]

        # We eliminate these regions from the dictionary of border regions
        del diagrams_tangles[label_2][1]['top_right_in']
        del diagrams_tangles[label_2][1]['top_right_out']

        # We check if they are also border region on another angle 
        # (this appens if we started from a 1/1 rational tangle)
        another_border_region = check_another_border_region('top_right_in', 'top_right_out', diagrams_tangles, label_2)

        if another_border_region:

            more_than_one_border_component[label_2] = another_border_region




    regions_to_glue = dict()

    regions_to_glue['region_in_1'] = region_in_1
    regions_to_glue['region_out_1'] = region_out_1
    regions_to_glue['region_in_2'] = region_in_2
    regions_to_glue['region_out_2'] = region_out_2
    regions_to_glue['more_than_one_border_component'] = more_than_one_border_component

    return regions_to_glue



















def check_another_border_region(region_in, region_out, diagrams_tangles, label_tangle):

    output = dict()

    if region_in in diagrams_tangles[label_tangle][1]['common_border_region'].keys():

        output['other_region_in'] = diagrams_tangles[label_tangle][1]['common_border_region'][region_in]


    if region_out in diagrams_tangles[label_tangle][1]['common_border_region'].keys():

        output['other_region_out'] = diagrams_tangles[label_tangle][1]['common_border_region'][region_out]


    return output 






def gluing_1_1(p_1, q_1, p_2, q_2, label_1, label_2, end_1, end_2, diagrams_tangles, tangles_input):
    

    # We identify the regions to glue together
    regions_to_glue = identify_regions_to_glue(end_1, end_2, label_1, label_2, diagrams_tangles)


    region_in_1 = regions_to_glue['region_in_1']
    region_out_1 = regions_to_glue['region_out_1']
    region_in_2 = regions_to_glue['region_in_2']
    region_out_2 = regions_to_glue['region_out_2']


    # We understand the signs of the tangles that we are gluing
    sign_1 = tangles_input[label_1 - 1][0]*'+' + (1 - tangles_input[label_1 - 1][0])*'-'
    sign_2 = tangles_input[label_2 - 1][0]*'+' + (1 - tangles_input[label_2 - 1][0])*'-'


    # We identify the regions to glue together
    regions_to_glue = identify_regions_to_glue(end_1, end_2, label_1, label_2, diagrams_tangles)

    region_in_1 = regions_to_glue['region_in_1']
    region_out_1 = regions_to_glue['region_out_1']
    region_in_2 = regions_to_glue['region_in_2']
    region_out_2 = regions_to_glue['region_out_2']



    # First we check if we are gluing 1/1 with another 1/1
    if (p_1 == 1) and (q_1 == 1) and (p_2 == 1) and (q_2 == 1):

        pass





    elif (p_1 == 1) and (q_1 == 1):

        if sign_1 == '+':

            if end_1 == 1:

                pass

            elif end_1 == 2:

                pass

            elif end_1 == 3:

                pass

            else:

                pass


        else:

            if end_1 == 1:

                pass

            elif end_1 == 2:

                pass

            elif end_1 == 3:

                pass

            else:

                pass



    elif (p_2 == 1) and (q_2 == 1):

        if sign_2 == '+':

            pass


        else:

            pass





    else:

        # Sanity check, we shouldn't have any other case
        sys.exit('Something wrong, we were about to glue a 1/1 rational tangle to something and suddenly we were not able to find this trivial tangle.')