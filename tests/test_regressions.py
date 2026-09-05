"""Regression tests for flag combinations that used to raise at run time."""

import pytest

import main
from functions.pipeline import nicefy


PRETZEL = 'inputs/tangles/pretzel_tangle.txt'
CLOSED = 'inputs/normal/closed_diagram.txt'


def run_cli(repository_root, tmp_path, *options):
    output_path = tmp_path / 'nicefied.txt'
    exit_code = main.main([str(repository_root / options[0]), '-o', str(output_path), *options[1:]])

    assert exit_code == 0
    return output_path.read_text()


def test_saving_only_the_final_diagram(repository_root, tmp_path):
    # Used to raise NameError: the final-diagram branch wrote a string that was
    # only bound inside the intermediate-steps branch
    written = run_cli(repository_root, tmp_path, CLOSED, '--save-final-diagram', '--no-save-intermediate-steps')

    assert written.count('FINAL DIAGRAM') == 1
    assert 'Step number' not in written


def test_saving_both_writes_the_final_diagram_once(repository_root, tmp_path):
    # Used to write the intermediate steps twice and the final diagram not at all
    written = run_cli(repository_root, tmp_path, PRETZEL, '--save-final-diagram', '--save-intermediate-steps')

    assert written.count('FINAL DIAGRAM') == 1

    # Two cycles, so steps 0 and 1 are reported and step 2 is the final diagram
    assert written.count('Step number 0:') == 1
    assert written.count('Step number 1:') == 1
    assert 'Step number 2:' not in written


def test_saving_only_the_intermediate_steps(repository_root, tmp_path):
    written = run_cli(repository_root, tmp_path, PRETZEL, '--no-save-final-diagram', '--save-intermediate-steps')

    assert 'FINAL DIAGRAM' in written

    # Nothing is written separately, so all three steps are reported here
    for step in range(3):
        assert f'Step number {step}:' in written


def test_saving_neither(repository_root, tmp_path):
    written = run_cli(repository_root, tmp_path, CLOSED, '--no-save-final-diagram', '--no-save-intermediate-steps')

    assert 'Number of generators of the diagram: 3' in written
    assert 'Step number' not in written


def test_a_run_that_needed_no_cycles_has_no_empty_step_section(repository_root, tmp_path):
    # The starting diagram is already the final one, so once it is written on
    # its own there is nothing left to report
    written = run_cli(repository_root, tmp_path, CLOSED, '--save-final-diagram', '--save-intermediate-steps')

    assert written.count('FINAL DIAGRAM') == 1
    assert 'These are the intermediate' not in written


def test_tangle_without_trying_basepoint_placements(repository_root, parameters):
    # Used to raise UnboundLocalError: this branch of input_manager referenced
    # the dictionary built by the other branch
    results = nicefy(
        repository_root / PRETZEL,
        parameters(try_multiplicity_zero_regions_choices=False),
    )

    # Only the placement named in the input file is tried, which for this
    # diagram happens to be one of the best
    assert results['number_of_generators'] == 82
    assert results['number_of_regions'] == 30


def test_a_missing_input_file_is_reported(repository_root, tmp_path, capsys):
    with pytest.raises(SystemExit) as exit_info:
        main.main([str(tmp_path / 'absent.txt')])

    assert exit_info.value.code == 2
    assert 'no such input file' in capsys.readouterr().err
