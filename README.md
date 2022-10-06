# aiida_eos

A demonstration of creating a Python package for AiiDA plugins.
The goal is to create a plugin package for the Equation of State workflow demonstrated in: <https://aiida-qe-demo.readthedocs.io/en/latest/6_write_your_own_workflow.html>.

Each commit in this repository corresponds to a step in the tutorial.

Note, <https://github.com/aiidateam/aiida-plugin-cutter> can be used to automate most of these steps,
but here we shall do it manually explain each aspect of the package.

## Initial creation

The first step is to create a new repository on GitHub.
We will call it `aiida_eos`.
The repository should be created with a `README.md` and a `.gitignore` file.

### Interacting with the repository

We shall use [Visual Studio Code](https://code.visualstudio.com/) to interact with the repository.
This is a free, open-source, cross-platform IDE, with nice integration with GitHub, and many useful extensions.

## Creating the package metadata

The first step is to create the package metadata.
This is done by creating a `pyproject.toml` file in the root of the repository.
This can be used by pip to install the package, and by other tools to build the package: <https://pip.pypa.io/en/stable/reference/build-system/pyproject-toml/>

We shall use [flit](https://flit.readthedocs.io/en/latest/) to build the package.
This is a simple tool that is designed to build Python packages from a `pyproject.toml` file.

We can initialise the `pyproject.toml` file by running:

```bash
flit init
```

This also generates a license file, which is crucial for allowing others to use your package.
