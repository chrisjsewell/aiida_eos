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

## Create the package and install it

We create the initial package with a single file: `src/aiida_eos/__init__.py`.
This file should have a docstring that describes the package, and a `__version__` variable.

We now want to install the package in editable mode.
This means that we can make changes to the package, and they will be immediately available to Python.

First we create a [virtual environment](https://packaging.python.org/en/latest/tutorials/installing-packages/#creating-and-using-virtual-environments), and activate it:

```bash
python -m venv .venv
source .venv/bin/activate
```

Virtual environments are a way of isolating Python environments.

We can now install the package in editable mode:

```bash
python -m pip install --upgrade pip
pip install -e .
```

We can now import the package in Python:

```python
>>> import aiida_eos
>>> aiida_eos.__version__
'0.0.1'
```

## Adding formatting and linting with pre-commit

We shall use [pre-commit](https://pre-commit.com/) to automatically format and lint the code.
This will ensure that the code is formatted consistently, and that it conforms to the style guide.

We can initialise a pre-commit configuration file with:

```bash
pre-commit sample-config > .pre-commit-config.yaml
pre-commit autoupdate
pre-commit install
```

We shall add a few additional hooks to the configuration file:

- `black`: a Python code formatter
- `flake8`: a Python linter
- `isort`: a tool to sort the Python imports

## Adding testing

We shall use [pytest](https://docs.pytest.org/en/latest/) to run tests on our package.
To install pytest, we shall add it to an `optional-dependencies` section in the `pyproject.toml` file.
This is because we only need pytest to run the tests, and not to use the package.

We can now install the package, with the optional dependencies:

```bash
pip install -e ".[test]"
```

We can now add a test to the package.
We shall add a test that checks that the package can be imported.
This is done by adding a `tests` directory, and a `test_import.py` file in it.

Now we can run the tests:

```bash
pytest
```

To check the coverage of the tests, we can run:

```bash
pytest --cov=aiida_eos
```

### Using tox

The [tox](https://tox.readthedocs.io) CLI tool is an optional way to automate both setting up the virtual environment, then running the tests within it.
See the `pyproject.toml` section for the configuration.
You can then simply run `tox` to run the tests, or `tox -e py39` to run with a certain python version.
See [tox-conda](https://tox-conda.readthedocs.io) for an example of how to use tox with conda.

### Adding GitHub Actions

We can use [GitHub Actions](https://github.com/features/actions) to automatically run the tests on each commit.
This is done by adding a `.github/workflows/test.yml` file.

## Adding the rescale calcfunction

We shall add a `rescale` calcfunction to the package.
This is a simple function that takes a structure, and rescales it by a given factor.

Note that up until now, we have not added any AiiDA specific code.
Now that we want to add an AiiDA specific calcfunction, we need to add the `aiida-core` dependency to the `pyproject.toml` file, and also `ase` for the structure manipulation.

If using `tox`, we can regenerate our virtual environment with:

```bash
tox -r
```

### Type annotations

We will also notice that we added type annotations to the function.
This is a good practice, to provide static type inference, and also allows us to use tools like [mypy](http://mypy-lang.org/) to check the type annotations.

### Testing the calcfunction

We can now add a test for the `rescale` calcfunction.
In fact, if we were to use test-driven development, we would first write the test, and then write the code to make the test pass!

Since the calcfunction needs to store data to an AiiDa profile, we need to create a profile for the tests.
We can do this by utilising the [pgtest package](https://pypi.org/project/pgtest/) to create a temporary, local PostgreSQL database cluster, which allows us to create a temporary AiiDA profile, which we add to the `pyproject.toml` test dependencies.

For this we will first need an [PostgreSQL](https://www.postgresql.org/) server running, with which to connect.
There are numerous ways to do this, such as using the [Docker image](https://hub.docker.com/_/postgres), or installing via [Homebrew](https://brew.sh/) on macOS, or via the [PostgreSQL apt repository](https://www.postgresql.org/download/linux/ubuntu/) on Ubuntu.

To create the profile for the tests, we can add a `conftest.py` file to the `tests` directory.
Then we register the AiiDA [pytest fixtures](https://docs.pytest.org/en/6.2.x/fixture.html) in it.
You can see all the available fixtures by running `pytest --fixtures` (or `tox -- --fixtures`).
The initial one we need is the `aiida_profile_clean` fixture, which creates a temporary profile, and tears it down at the end of the test.

We can now add a passing test for the `rescale` calcfunction.

### Setting up PostgreSQL on GitHub Actions

We also need to start a PostgreSQL server for our GitHub Actions, by specifying a service in the `test.yml` file.
This actually uses the [PostgreSQL Docker image](https://hub.docker.com/_/postgres), which is started before the tests are run.
