"""The Equation of State (EoS) workflow."""
from aiida import engine, orm
from aiida_quantumespresso.calculations.pw import PwCalculation

from .rescale import rescale


class EquationOfState(engine.WorkChain):
    """WorkChain to compute Equation of State using Quantum ESPRESSO."""

    @classmethod
    def define(cls, spec: engine.ProcessSpec):
        """Specify inputs and outputs."""
        super().define(spec)
        spec.input(
            "code",
            valid_type=orm.Code,
        )
        spec.input("pseudo_family_label", valid_type=orm.Str)
        spec.input("structure", valid_type=orm.StructureData)
        spec.input("scale_factors", valid_type=orm.List)
        spec.outline(
            cls.run_eos,
            cls.results,
        )
        spec.output("eos", valid_type=orm.Dict)

    def run_eos(self):
        """Run calculations for equation of state."""
        # Create basic structure and attach it as an output
        structure = self.inputs.structure

        pseudo_family = orm.load_group(self.inputs.pseudo_family_label.value)

        self.ctx.labels = [
            f"c{idx}" for idx, _ in enumerate(self.inputs.scale_factors.get_list())
        ]

        for label, factor in zip(self.ctx.labels, self.inputs.scale_factors.get_list()):

            rescaled_structure = rescale(structure, orm.Float(factor))
            inputs = generate_scf_input_params(
                rescaled_structure, self.inputs.code, pseudo_family
            )

            self.report(
                "Running an SCF calculation for {} with scale factor {}".format(
                    structure.get_formula(), factor
                )
            )

            # Ask the workflow to continue when the results are ready,
            # and store them in the context
            calc_future = self.submit(PwCalculation, **inputs)
            self.to_context(**{label: calc_future})

    def results(self):
        """Process results."""
        inputs = {}
        for label in self.ctx.labels:
            calcnode: orm.CalcJobNode = self.ctx[label]
            inputs[label] = calcnode.base.links.get_outgoing().get_node_by_label(
                "output_parameters"
            )
        eos = create_eos_dictionary(**inputs)

        # Attach Equation of State results as output node to be able to plot the EOS later
        self.out("eos", eos)


@engine.calcfunction
def create_eos_dictionary(**kwargs: orm.Dict) -> orm.Dict:
    """Create a single `Dict` node from the `Dict` output parameters of completed `PwCalculations`.

    The dictionary will contain a list of tuples,
    where each tuple contains the volume, total energy,
    and its units of the results of a calculation.
    """
    eos = [
        (result.dict.volume, result.dict.energy, result.dict.energy_units)
        for label, result in kwargs.items()
    ]
    return orm.Dict(dict={"eos": eos})


def generate_scf_input_params(
    structure: orm.StructureData, code: orm.Code, pseudo_family
) -> engine.ProcessBuilder:
    """Construct a builder for the `PwCalculation` class and populate its inputs."""
    parameters = {
        "CONTROL": {
            "calculation": "scf",
            "tstress": True,  # Important that this stays to get stress
            "tprnfor": True,
        },
        "SYSTEM": {
            "ecutwfc": 30.0,
            "ecutrho": 200.0,
        },
        "ELECTRONS": {
            "conv_thr": 1.0e-6,
        },
    }

    kpoints = orm.KpointsData()
    kpoints.set_kpoints_mesh([2, 2, 2])

    builder = code.get_builder()
    builder.code = code
    builder.structure = structure
    builder.kpoints = kpoints
    builder.parameters = orm.Dict(dict=parameters)
    builder.pseudos = pseudo_family.get_pseudos(structure=structure)
    builder.metadata.options.resources = {"num_machines": 1}
    builder.metadata.options.max_wallclock_seconds = 30 * 60

    return builder
