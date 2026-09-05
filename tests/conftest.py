import sys
from pathlib import Path

import pytest

# The packages live at the repository root, next to main.py
REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPOSITORY_ROOT))

from main import build_parser  # noqa: E402


@pytest.fixture
def repository_root():
    return REPOSITORY_ROOT


@pytest.fixture
def parameters():
    """Return a factory for run parameters holding the command line defaults.

    Building them through the parser rather than by hand keeps the tests honest
    about what an actual invocation does, and fails loudly if an option is
    renamed. Printing is turned off so the tests stay quiet.
    """

    def make(**overrides):
        defaults = vars(build_parser().parse_args(['unused'])).copy()
        defaults.pop('input_path')
        defaults.pop('output')

        defaults['print_details_nicefication'] = False
        defaults['print_output_for_PQM'] = False

        defaults.update(overrides)
        return defaults

    return make
