![logo](doc/_static/piezosystem_logo.svg)

# PySoWorks

[![PyPI - Version](https://img.shields.io/pypi/v/pysoworks)](https://pypi.org/project/pysoworks/)
[![Python Versions](https://img.shields.io/pypi/pyversions/pysoworks)](https://pypi.org/project/pysoworks/)
[![Windows Binary](https://img.shields.io/github/v/release/piezosystemjena/PySoWorks?label=EXE)](https://github.com/piezosystemjena/PySoWorks/releases/latest/)
[![Publish Python Package](https://github.com/piezosystemjena/PySoWorks/actions/workflows/publish-pypi.yml/badge.svg)](https://github.com/piezosystemjena/PySoWorks/actions/workflows/publish-pypi.yml)
[![Build Windows Executable](https://github.com/piezosystemjena/PySoWorks/actions/workflows/build-windows.yml/badge.svg)](https://github.com/piezosystemjena/PySoWorks/actions/workflows/build-windows.yml)

PySoWorks is an application for controlling the piezo amplifiers, such as the [NV200/D](https://www.piezosystem.com/product/nv-200-d-compact-amplifier/), from [piezosystem jena](https://www.piezosystem.com/) GmbH. It demonstrates the use of the [NV200 Python library](https://pypi.org/project/nv200/) within a graphical interface based on PySide6.

![PySoWorks UI](doc/images/pysoworks_ui.png)

## For Users

## Features 

- GUI based on PySide6
- Support for NV200 hardware control
- Supports control of multiple devices
- Dark mode theming

### Quick Install

Install from **PyPI**:

```shell
pip install pysoworks
```

### Install in a Virtual Environment (Recommended)

Using venv (built-in Python module):

```shell
# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install pysoworks from PyPI
pip install pysoworks
```

### Usage

Once installed, you can launch the application from the terminal:

```shell
pysoworks
```

## For Developers

This project uses [Poetry](https://python-poetry.org/) for Python dependency management, packaging, and publishing. Poetry provides a modern, streamlined alternative to `pip` and `virtualenv`, handling everything from installing dependencies to building and publishing the package.

If you're contributing to the project or running it locally for development, the steps below will help you set up your environment.

### Installing poetry

If necessary, install [poetry] according to the official [installation instructions](https://python-poetry.org/docs/#installation) 
(it's recommended to use [pipx](https://github.com/pypa/pipx) to install poetry in its own isolated environment but still have it available as a system wide command).

```shell
pip install pipx
pipx ensurepath
# reload your shell or start a new instance
pipx install poetry
```

### Use an In-Project Virtual Environment (Optional)

By default, Poetry creates virtual environments in `{cache-dir}/virtualenvs`
(Windows: `%USERPROFILE%/AppData/Local/pypoetry/Cache/virtualenvs`).

You can instead configure Poetry to create the virtual environment inside the project directory by setting:

```shell
poetry config virtualenvs.in-project true
```

This will place the virtualenv in a `.venv` folder at the project root the next time you run `poetry install`.

Now, when we run `poetry install` in a project directory, it will create and install all dependencies 
(and the project itself) into an in-project virtualenv located in `{project-root}/.venv`.

> **Note:**  
> If you already have an existing environment in the default location (i.e. out-of-project) and would like to convert to an in-project virtualenv, you have to first remove the existing virtualenv, ensure that the `virtualenvs.in-project` option is set to `true` and then create the new in-project virtualenv using `poetry install` (see [below](#installing-dependencies)) again.
> 
> To remove the existing virtualenv, first get its name and then remove it:
> 
> ```shell
> poetry env list   # note the name of the environment
> poetry env remove <name>
> ```
> 
> If you're sure you only have one environment, you can also just use `poetry env remove --all`.


### Installing dependencies

#### Required dependencies

To install all required dependencies and set up the project in editable mode:

```shell
poetry install
```

To skip installing the project itself (i.e. install only dependencies):

```shell
poetry install --no-root
```

#### Optional dependencies

Some extra features are provided via optional dependencies.

- Install all **optional packages**:

```shell
poetry install --all-extras
```

- Install **specific extras**:

```shell
poetry install --extras "extra1 extra2"
# or
poetry install -E extra1 -E extra2
```

## Building and Publishing

### Build the Wheel

To build a distributable `.whl` package:

```shell
poetry build
```

This creates a `.whl` and `.tar.gz` file in the `dist/` directory.

### Publishing 

#### To TestPyPI

```shell
poetry build
poetry config repositories.test-pypi https://test.pypi.org/legacy/
poetry config pypi-token.test-pypi your-token-here
poetry publish -r test-pypi
```

If you would like to test the installation from TestPyPi, you should use the
following command:

```shell
pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple pysoworks
```

 This avoids dependency resolution issues by:

- Getting your test package (pysoworks) from **Test PyPI**
- Getting all other packages (e.g., matplotlib, pyside6, etc.) from **PyPI**

#### To PyPI

```shell
poetry build
poetry config repositories.pypi https://upload.pypi.org/legacy/
poetry config pypi-token.pypi your-token-here
poetry publish -r test-pypi
```


### Building a Standalone Executable with PyInstaller

You can create a standalone executable of PySoWorks using PyInstaller.

Make sure PyInstaller is installed in your environment:

```shell
pip install pyinstaller
```

Build the executable using the provided spec file:

```shell
pyinstaller --clean --log-level=DEBUG pysoworks.spec
```

- `--clean` clears any temporary PyInstaller files before building.

- `--log-level=DEBUG` enables detailed logging to help diagnose any build issues.

The resulting executable will be located in the `dist/` directory.

