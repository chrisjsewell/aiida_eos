from aiida import engine, orm


@engine.calcfunction
def rescale(structure: orm.StructureData, scale: orm.Float) -> orm.StructureData:
    """Rescale a structure's unit cell."""
    ase_structure = structure.get_ase()
    scale_value = scale.value

    new_cell = ase_structure.get_cell() * scale_value
    ase_structure.set_cell(new_cell, scale_atoms=True)

    return orm.StructureData(ase=ase_structure)
