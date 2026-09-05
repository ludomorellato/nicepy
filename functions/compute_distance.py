from collections import deque


def compute_distance(diagram):
    """Label every region with its distance from the nearest basepoint, in place.

    The distance of a region is the smallest number of beta circles an arc must
    cross to reach a multiplicity zero region, travelling in the complement of
    the alpha curves (Definition 4.13 of the thesis, extended to several
    basepoints in Section 4.4.2). Crossing an alpha edge is not allowed, so the
    walk only ever steps between regions that share a beta edge.

    A breadth-first search seeded with every basepoint at once gives each region
    the distance to the nearest of them. For a tangle diagram each region also
    records, in p_or_q, which side of the alpha arcs the basepoint it was
    reached from lies on.
    """

    regions = diagram.regions

    # The regions holding a basepoint are the ones at distance 0, and they are
    # the sources the search starts from
    frontier = deque()

    if diagram.is_tangle_diagram:
        for couple in diagram.basepoints_p_or_q:
            region = regions[couple[0]]
            region.distance = 0
            region.p_or_q = ((1 - couple[1]) * 'p') + (couple[1] * 'q')
            frontier.append(region)
    else:
        for index in diagram.multiplicity_zero_regions:
            regions[index].distance = 0
            frontier.append(regions[index])

    # Seeding the queue with every basepoint before expanding any of them is
    # what makes the result the distance to the *nearest* basepoint: regions are
    # settled in order of increasing distance, so the first label a region gets
    # is the smallest one it can get
    while frontier:

        region = frontier.popleft()

        for neighbor, edge in region.blue_neighbors:

            if neighbor.distance == -1:

                neighbor.distance = region.distance + 1

                # We also assign the p_or_q value to the region
                if diagram.is_tangle_diagram:
                    neighbor.p_or_q = region.p_or_q

                frontier.append(neighbor)
