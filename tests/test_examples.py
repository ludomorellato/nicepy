"""End-to-end tests over the committed example diagrams."""

import pytest

from functions.pipeline import nicefy


# The counts every example is known to produce. They match the reference output
# committed under examples/expected_output/.
EXAMPLES = [
    ('inputs/normal/closed_diagram.txt', 3, 3, 0),
    ('inputs/normal/bordered_sutured_diagram.txt', 120, 22, 2),
    ('inputs/rational/rational_tangle.txt', 20, 22, 0),
    pytest.param(
        'inputs/rational/sum_of_rational_tangles.txt', 398, 44, 4,
        marks=pytest.mark.slow,
    ),
    ('inputs/tangles/pretzel_tangle.txt', 82, 30, 2),
]

EXAMPLE_IDS = [
    'closed', 'bordered_sutured', 'rational', 'sum_of_rationals', 'pretzel',
]


def assert_diagram_is_nice(diagram):
    """Check the postcondition of the Sarkar-Wang algorithm.

    A diagram is nice when every region that does not contain a basepoint is a
    bigon or a square. A region carries distance 0 exactly when it holds a
    basepoint, and Region.badness is max(n - 2, 0) for a region with 2n edges,
    so badness 0 means at most four edges. We check the regions themselves
    rather than the diagram's own is_nice flag, which the algorithm sets on
    itself and so cannot corroborate its own result.
    """

    for label, region in diagram.regions.items():
        assert region.distance >= 0, (
            f'region {label} was never reached from a basepoint'
        )

        if region.distance > 0:
            assert region.badness == 0, (
                f'region {label} is at distance {region.distance} from a '
                f'basepoint and has badness {region.badness}: it is neither a '
                f'bigon nor a square, so the diagram is not nice'
            )


@pytest.mark.parametrize(
    'input_path, generators, regions, cycles', EXAMPLES, ids=EXAMPLE_IDS,
)
def test_example_is_nicefied(repository_root, parameters, input_path, generators, regions, cycles):
    results = nicefy(repository_root / input_path, parameters())

    assert results['number_of_generators'] == generators
    assert results['number_of_regions'] == regions
    assert results['number_iteration_algorithm'] == cycles

    assert_diagram_is_nice(results['H_diagram'])


@pytest.mark.parametrize(
    'input_path, generators, regions, cycles', EXAMPLES, ids=EXAMPLE_IDS,
)
def test_intermediate_steps_end_at_the_final_diagram(
    repository_root, parameters, input_path, generators, regions, cycles,
):
    results = nicefy(repository_root / input_path, parameters())

    # One diagram is recorded per cycle, plus the starting diagram
    assert sorted(results['intermediate_steps']) == list(range(cycles + 1))
    assert results['intermediate_steps'][cycles] is results['H_diagram']
