"""Configuration for pytest."""
import json
from pathlib import Path

from aiida import orm
from aiida_pseudo.cli.install import download_sssp
from aiida_pseudo.cli.utils import create_family_from_archive
from aiida_pseudo.groups.family import SsspConfiguration, SsspFamily
import pytest

pytest_plugins = ["aiida.manage.tests.pytest_fixtures"]


def pytest_addoption(parser):
    """Define pytest command-line."""
    group = parser.getgroup("aiida_eos")
    group.addoption(
        "--pwx-exec",
        dest="pwx_exec",
        default="pw.x",
        help=("Specify a the pw.x executable path."),
    )


def pytest_report_header(config):
    """Add header information for pytest execution."""
    return [
        f'pw.x executable: {config.getoption("pwx_exec")}',
    ]


@pytest.fixture(scope="function")
def pwx_code(aiida_local_code_factory, pytestconfig):
    return aiida_local_code_factory(
        executable=pytestconfig.getoption("pwx_exec"),
        entry_point="quantumespresso.pw",
        prepend_text="export OMP_NUM_THREADS=1",
    )


@pytest.fixture(scope="function")
def si_structure():
    cell = [
        [3.7881476451529, 0.0, 0.0],
        [1.8940738225764, 3.2806320939886, 0.0],
        [1.8940738225764, 1.0935440313296, 3.0930096003167],
    ]
    structure = orm.StructureData(cell=cell)
    structure.append_atom(position=(0.0, 0.0, 0.0), symbols="Si")
    structure.append_atom(
        position=(1.8940738225764, 1.0935440313296, 0.77325240007918), symbols="Si"
    )
    structure.store()
    return structure


@pytest.fixture(scope="function")
def sssp_pseudos():
    """Load the SSSP pseudopotentials."""
    config = SsspConfiguration(version="1.1", functional="PBE", protocol="efficiency")
    label = SsspFamily.format_configuration_label(config)

    pseudos = Path(__file__).parent / "sssp_pseudos"
    pseudos.mkdir(exist_ok=True)

    filename = label.replace("/", "-")

    if not (pseudos / (filename + ".tar.gz")).exists():
        download_sssp(
            config, pseudos / (filename + ".tar.gz"), pseudos / (filename + ".json")
        )

    family = create_family_from_archive(
        SsspFamily,
        label,
        pseudos / (filename + ".tar.gz"),
    )
    family.set_cutoffs(
        {
            k: {i: v[i] for i in ["cutoff_wfc", "cutoff_rho"]}
            for k, v in json.loads((pseudos / (filename + ".json")).read_text()).items()
        },
        "normal",
        unit="Ry",
    )
    return family
