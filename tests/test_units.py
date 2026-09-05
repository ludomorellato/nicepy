"""Unit tests for the self-contained helpers on the algorithm's hot path."""

import pytest

from classes.region_class import Region
from functions.compute_distance_complexities_diagram import compute_distance_complexities_diagram
from functions.compute_distance import compute_distance
from functions.get_index_of_edge import get_index_of_edge


class TestGetIndexOfEdge:
    """A region is a cyclic walk, so its edges wrap around the end of the list."""

    def test_finds_an_edge_in_the_middle(self):
        assert get_index_of_edge([1, 2, 3, 4], [2, 3]) == 1

    def test_finds_the_first_edge(self):
        assert get_index_of_edge([1, 2, 3, 4], [1, 2]) == 0

    def test_finds_the_edge_that_closes_the_walk(self):
        assert get_index_of_edge([1, 2, 3, 4], [4, 1]) == 3

    def test_is_directed(self):
        # [3, 2] is the same edge travelled the other way, and belongs to the
        # region on the other side of it
        with pytest.raises(SystemExit):
            get_index_of_edge([1, 2, 3, 4], [3, 2])

    def test_finds_the_first_occurrence_when_a_point_repeats(self):
        # An alpha circle may pass through the same intersection point twice
        assert get_index_of_edge([1, 2, 1, 3], [1, 3]) == 2

    def test_exits_when_the_edge_is_absent(self):
        with pytest.raises(SystemExit):
            get_index_of_edge([1, 2, 3, 4], [1, 4])


class DiagramStub:
    """The only attribute compute_distance_complexities_diagram reads."""

    def __init__(self, distance_complexities):
        self.distance_complexities = distance_complexities


def region_with_badness(label, badness):
    # Region takes half the number of edges and derives badness as max(n - 2, 0)
    region = Region(label, badness + 2, [], [], [], [])
    assert region.badness == badness
    return region


class TestComputeDistanceComplexitiesDiagram:

    def test_orders_regions_by_decreasing_badness_and_totals_each_distance(self):
        mild = region_with_badness(1, 1)
        severe = region_with_badness(2, 3)
        distant = region_with_badness(3, 2)

        complexities, total = compute_distance_complexities_diagram(
            DiagramStub({1: [mild, severe], 2: [distant]})
        )

        # Each entry is the summed badness of that distance, followed by the
        # regions paired with their negated badness, worst first
        assert complexities[1] == [4, (-3, severe), (-1, mild)]
        assert complexities[2] == [2, (-2, distant)]

        # Badness at distance d is weighted by 3**d, so the algorithm always
        # prefers to clear up regions far from the basepoints first
        assert total == 4 * 3 + 2 * 9

    def test_orders_by_distance(self):
        complexities, _ = compute_distance_complexities_diagram(
            DiagramStub({3: [region_with_badness(1, 1)], 1: [region_with_badness(2, 1)]})
        )

        assert list(complexities) == [1, 3]

    def test_a_nice_diagram_has_no_complexity(self):
        complexities, total = compute_distance_complexities_diagram(DiagramStub({}))

        assert complexities == {}
        assert total == 0


class DiagramForDistance:
    """The attributes compute_distance reads and writes."""

    def __init__(self, labels, blue_edges, basepoints, p_or_q=None):
        self.regions = {label: Region(label, 2, [], [], [], []) for label in labels}

        for first, second in blue_edges:
            self.regions[first].blue_neighbors.append((self.regions[second], [first, second]))
            self.regions[second].blue_neighbors.append((self.regions[first], [second, first]))

        self.multiplicity_zero_regions = basepoints
        self.basepoints_p_or_q = p_or_q or []
        self.is_tangle_diagram = bool(p_or_q)

    def distances(self):
        return {label: region.distance for label, region in self.regions.items()}


class TestComputeDistance:
    """Distance is how many beta edges away a region is from a basepoint.

    It is what orders the algorithm's work: badness at distance d is weighted
    by 3**d, so the worst region furthest from the basepoints is fixed first.
    """

    def test_walks_outwards_along_a_chain(self):
        diagram = DiagramForDistance([1, 2, 3, 4], [(1, 2), (2, 3), (3, 4)], [1])

        compute_distance(diagram)

        assert diagram.distances() == {1: 0, 2: 1, 3: 2, 4: 3}

    def test_does_not_depend_on_where_the_basepoint_sits_in_the_chain(self):
        diagram = DiagramForDistance([1, 2, 3, 4], [(1, 2), (2, 3), (3, 4)], [4])

        compute_distance(diagram)

        assert diagram.distances() == {1: 3, 2: 2, 3: 1, 4: 0}

    def test_takes_the_shorter_of_two_routes(self):
        # 4 is two steps away whichever way round the diamond you go
        diagram = DiagramForDistance([1, 2, 3, 4], [(1, 2), (1, 3), (2, 4), (3, 4)], [1])

        compute_distance(diagram)

        assert diagram.distances() == {1: 0, 2: 1, 3: 1, 4: 2}

    def test_a_shortcut_is_taken(self):
        # Round a five-cycle, 4 is reachable in two steps the short way (1-5-4)
        # even though the long way round (1-2-3-4) is three
        diagram = DiagramForDistance(
            [1, 2, 3, 4, 5], [(1, 2), (2, 3), (3, 4), (4, 5), (1, 5)], [1],
        )

        compute_distance(diagram)

        assert diagram.distances() == {1: 0, 2: 1, 3: 2, 4: 2, 5: 1}

    def test_a_tangle_diagram_carries_p_and_q_outwards(self):
        # Every region records which of the two basepoints it was reached from
        diagram = DiagramForDistance(
            [1, 2, 3, 4], [(1, 2), (2, 3), (3, 4)], [1, 4], p_or_q=[[1, 0], [4, 1]],
        )

        compute_distance(diagram)

        assert diagram.distances() == {1: 0, 2: 1, 3: 1, 4: 0}
        assert [diagram.regions[label].p_or_q for label in (1, 2, 3, 4)] == ['p', 'p', 'q', 'q']

    def test_with_two_basepoints_the_distance_is_to_the_nearest_one(self):
        """Section 4.4.2: the distance is measured to *some* basepoint, the nearest.

        Region 4 neighbours basepoint 5 directly, so it is at distance 1 even
        though the walk from basepoint 1 would reach it in three steps.
        """

        diagram = DiagramForDistance(
            [1, 2, 3, 4, 5], [(1, 2), (2, 3), (3, 4), (4, 5)], [1, 5],
        )

        compute_distance(diagram)

        assert diagram.distances() == {1: 0, 2: 1, 3: 2, 4: 1, 5: 0}

    def test_a_region_no_basepoint_can_reach_keeps_its_initial_label(self):
        # The thesis requires every component of the complement of alpha to hold
        # a multiplicity zero region, so this should not arise for valid input;
        # it must terminate rather than hang if it ever does
        diagram = DiagramForDistance([1, 2, 3], [(1, 2)], [1])

        compute_distance(diagram)

        assert diagram.distances() == {1: 0, 2: 1, 3: -1}
