"""Test that rescaling works as expected."""
from aiida import orm
from aiida_eos.rescale import rescale
import pytest


@pytest.mark.usefixtures("aiida_profile_clean")
def test_rescale():
    """Test that rescaling works as expected."""
    structure = orm.StructureData(cell=[[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    scale = orm.Float(2.0)
    scaled_structure = rescale(structure, scale)

    assert isinstance(scaled_structure, orm.StructureData)
    assert scaled_structure.cell == [[2, 0, 0], [0, 2, 0], [0, 0, 2]]
