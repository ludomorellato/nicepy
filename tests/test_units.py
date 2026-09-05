"""Unit tests for the self-contained helpers on the algorithm's hot path."""

import pytest

from classes.region_class import Region
from functions.compute_distance_complexities_diagram import compute_distance_complexities_diagram
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
