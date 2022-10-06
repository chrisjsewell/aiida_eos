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
