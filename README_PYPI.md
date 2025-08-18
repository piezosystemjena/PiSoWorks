# PySoWorks

![PyPI - Version](https://img.shields.io/pypi/v/pysoworks)
![Python Versions](https://img.shields.io/pypi/pyversions/pysoworks)
[![Docs](https://img.shields.io/badge/docs-online-success)](https://piezosystemjena.github.io/PySoWorks/)

PySoWorks is an application for controlling the piezo amplifiers, such as the [NV200/D](https://www.piezosystem.com/product/nv-200-d-compact-amplifier/), 
from [piezosystem jena](https://www.piezosystem.com/) GmbH. It demonstrates the use of the 
[NV200 Python library](https://pypi.org/project/nv200/) within a graphical interface based on PySide6.

The application shows how to use the [NV200 Python Library](https://pypi.org/project/nv200/) in a graphical user interface.

![pysoworks GUI](https://raw.githubusercontent.com/piezosystemjena/PySoWorks/refs/heads/main/doc/images/pysoworks_ui.png)

---

## Installation

### Quick Installation

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

## Usage

Once installed, you can launch the application from the terminal:

```shell
pysoworks
```

## Features 

- GUI based on PySide6
- Support for NV200 hardware control
- Supports control of multiple devices
- Dark mode theming
