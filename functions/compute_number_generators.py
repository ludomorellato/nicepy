import numpy
import itertools
import sys

def compute_number_generators(diagram):
    
    # In this function we compute the number of generator of the diagram
    # This means to construct a matrix nxn, where n is the number of the
    # circles of the diagram, to put in the place ij the number of 
    # intersection points of the i-th alpha circle and the j-th beta 
    # circle and then to compute the determinant of such matrix without
    # signs

    if diagram.red_arcs:

        # In this case, we need to construct the matrix in a slight different way
        # We have to construct \binomial((#beta circles - # alpha circles)/#alpha arcs) matrices, 
        # where we make them square by adding all the possible combinations of alpha arcs at the 
        # end and we sum of determinants (without signs) of all these matrices

        # We count the number of the blue/red circles
        number_blue_circles = len(diagram.blue_circles)
        number_red_circles = len(diagram.red_circles)
        
        number_arcs_to_square =  number_blue_circles -  number_red_circles

        combinations = [comb for comb in itertools.combinations(list(range(len(diagram.red_arcs))), number_arcs_to_square)]
        
        total_number_generators = 0

        for comb in combinations:

            # We construct the list of red curves for this combination
            red_arcs_temp = [diagram.red_arcs[index] for index in comb]

            red_curves_temp = red_arcs_temp + diagram.red_circles

            # We start with an empty matrix
            intersection_matrix_temp = []
            
            # We construct the rows, one row is one blue circle
            for blue_circle in diagram.blue_circles:

                row_temp = []

                # We take a set with for the blue circle
                blue_circle_set = set(blue_circle)

                for red_curve in red_curves_temp:

                    # We take a set with for the red circle
                    red_curve_set = set(red_curve)

                    # We intersect the two sets
                    intersection_number_temp = len(red_curve_set.intersection(blue_circle_set))

                    row_temp.append(intersection_number_temp)

                
                intersection_matrix_temp.append(row_temp)

            
            # We compute the determinant without signs
            # We distinguish the case in which we only have one alpha circle and one beta circle
            if len(intersection_matrix_temp) == 1:
                return intersection_matrix_temp[0][0]

            else:
                number_generators_temp = determinant_without_sign(intersection_matrix_temp)

                #print('The number of generators for this diagram is: ' + str(number_generators))

                total_number_generators = total_number_generators + number_generators_temp
            
        
        return total_number_generators


    else:

        # We start with an empty matrix
        intersection_matrix = []

        # We count the number of the blue/red circles
        number_circles = len(diagram.blue_circles)
        
        # We construct the rows, one row is one circle
        for blue_circle in diagram.blue_circles:

            row_temp = []

            # We take a set with for the blue circle
            blue_circle_set = set(blue_circle)

            for red_circle in diagram.red_circles:

                # We take a set with for the red circle
                red_circle_set = set(red_circle)

                # We intersect the two sets
                intersection_number_temp = len(red_circle_set.intersection(blue_circle_set))

                row_temp.append(intersection_number_temp)

            
            intersection_matrix.append(row_temp)



        # Sanity check
        # We check that the sum of all the entries in the matrix is the 
        # same of the number of intersection point in the diagram

        check_number = 0

        for row in intersection_matrix:
            check_number = check_number + sum(row)


        if check_number != diagram.number_intersection_points:
            sys.exit("Error: the number of points in the diagram doesn't agree with the computation")

        
        # We compute the determinant without signs
        # We distinguish the case in which we only have one alpha circle and one beta circle
        if len(intersection_matrix) == 1:
            return intersection_matrix[0][0]

        else:
            number_generators = determinant_without_sign(intersection_matrix)

            #print('The number of generators for this diagram is: ' + str(number_generators))

            return(number_generators)





def copy_matrix(M):
    """
    Creates and returns a copy of a matrix.
        :param M: The matrix to be copied
        :return: A copy of the given matrix
    """
    # Section 1: Get matrix dimensions
    rows = len(M)
    cols = len(M[0])

    # Section 2: Create a new matrix of zeros
    MC = zeros_matrix(rows, cols)

    # Section 3: Copy values of M into the copy
    for i in range(rows):
        for j in range(cols):
            MC[i][j] = M[i][j]

    return MC







def zeros_matrix(rows, cols):
    """
    Creates a matrix filled with zeros.
        :param rows: the number of rows the matrix should have
        :param cols: the number of columns the matrix should have
        :return: list of lists that form the matrix
    """
    M = []
    while len(M) < rows:
        M.append([])
        while len(M[-1]) < cols:
            M[-1].append(0.0)

    return M





def determinant_without_sign(A, total=0):
    # Section 1: store indices in list for row referencing
    indices = list(range(len(A)))
     
    # Section 2: when at 2x2 submatrices recursive calls end
    # We compute the 2x2 determinant WITHOUT SIGNS
    if len(A) == 2 and len(A[0]) == 2:
        val = A[0][0] * A[1][1] + A[1][0] * A[0][1]
        return val
 
    # Section 3: define submatrix for focus column and 
    #      call this function
    for fc in indices: # A) for each focus column, ...
        # find the submatrix ...
        As = copy_matrix(A) # B) make a copy, and ...
        As = As[1:] # ... C) remove the first row
        height = len(As) # D) 
 
        for i in range(height): 
            # E) for each remaining row of submatrix ...
            #     remove the focus column elements
            As[i] = As[i][0:fc] + As[i][fc+1:] 

        # We always have sign 1
        sign = 1 # F) 
        # G) pass submatrix recursively
        sub_det = determinant_without_sign(As)
        # H) total all returns from recursion
        total = total + sign * A[0][fc] * sub_det 
 
    return total