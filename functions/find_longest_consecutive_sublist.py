# Initially this function was thought for the search of a generalized handleslide, but it is not actually required


# Returns length of the longest
# contiguous subsequence
def find_longest_consecutive_sublist(arr, number_edges_region):
    
    # We set the output
    maximum_sublists = []
 
    # Sort the array
    arr.sort()

    # We save the maximum index
    maximum_index = arr[-1]

    # We add a copy of the list at the end of the 
    # list (in this way we consider also the modulo)
    arr = arr + arr 
    
    # We set a flag to know when we have finished the first cycle 
    # (and in such case, when we need to stop if we interrupt the consecutivness)
    stop_the_cycle = False

    # We take note of the lenght count
    maximum_lenght = 0

    # Find the maximum sublist
    # by traversing the array
    for index in range(len(arr) - 1):
        
        # We check if we already reached the last index for the first time
        if arr[index] == maximum_index:
            
            # In this case, we set the stop_the_cycle flag to True
            stop_the_cycle = True


        # If we are starting to count, we start the new list_temp
        if not list_temp:

            # We check if we need to stop the cycle or not
            if stop_the_cycle:
                break
            else:
                # We start a new search
                list_temp = [arr[index]]

        # We check if the next is consecutive
        if ((arr[index] + 2) % number_edges_region) == arr[index + 1]:

            # If so, we append it to list_temp
            list_temp.append(arr[index + 1])

        else:

            # if it is not, we stop the iteration on index
            maximum_sublists.append(list_temp)

            # We update the maximum lenght
            lenght_temp = len(list_temp)
            if lenght_temp > maximum_lenght:

                # We update the maximum lenght
                maximum_lenght = lenght_temp


            # We erase the temp list
            list_temp = []

            



    # We now have a list with sublists of different lenght and the data of the maximum lenght

    return maximum_sublists
 


d = {5: [54, 39], 7: [40, 20], 3: [11, 53], 9: [21, 22]}
list = d.keys()
number_edges_region = 10