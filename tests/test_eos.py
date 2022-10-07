"""Test that rescaling works as expected."""
from aiida import engine, orm
from aiida_eos.eos import EquationOfState
import pytest


@pytest.mark.usefixtures("aiida_profile_clean")
def test_eos(pwx_code, si_structure, sssp_pseudos):
    """Test that workchain works correctly."""
    eos_wc_result = engine.run_get_node(
        EquationOfState,
        code=pwx_code,
        pseudo_family_label=orm.Str(sssp_pseudos.label),
        structure=si_structure,
        scale_factors=orm.List(list=[1.0]),
    )
    assert eos_wc_result[1].is_finished_ok
