![logo](doc/_static/piezosystem_logo.svg)


# NV200 Python Lib

[![PyPI version](https://img.shields.io/pypi/v/nv200)](https://pypi.org/project/nv200/)
[![Python Version](https://img.shields.io/pypi/pyversions/nv200)](https://www.python.org/downloads/)
[![Docs](https://img.shields.io/badge/docs-online-success)](https://nv200-python-lib-e9158a.gitlab.io/)


The NV200 Python library allows you to control the [NV200/D piezo controller](https://www.piezosystem.com/product/nv-200-d-compact-amplifier/) from [piezosystem Jena](https://www.piezosystem.com) via Python.
The library supports the ethernet interface as well as the USB interface of the device.

![NV200](doc/images/nv200.jpg)

## Features

- Asynchronous communication via `aioserial` and `telnetlib3`
- Simple Pythonic interface for device control
- Query & set device position
- Supports NV200 data recorder functionality
- Easy interface for NV200 waveform generator


## For Users

### 📦 Quick Install

The NV200 library is available via [PyPI](https://pypi.org/project/nv200/) - the Python Package Index. To install the library, simply use pip:

```shell
pip install nv200
```


### 📚 Documentation 

Comprehensive documentation—including API reference, installation options, and usage examples—is available here:

[https://nv200-python-lib-e9158a.gitlab.io/](https://nv200-python-lib-e9158a.gitlab.io/)


### 🧪 Quick Example

```python
from nv200.device_types import DetectedDevice
from nv200.device_discovery import discover_devices
from nv200.device_interface import DeviceClient, create_device_client

async def main_async():
    print("Discovering devices...")
    detected_devices = await discover_devices()
    
    if not detected_devices:
        print("No devices found.")
        return

    # Create a device client for the first detected device
    device = create_device_client(detected_devices[0])
    await client.connect()

if __name__ == "__main__":
        asyncio.run(main_async())
```

## For Developers

This project uses [Poetry](https://python-poetry.org/) for Python dependency management, packaging, and publishing. Poetry provides a modern, streamlined alternative to `pip` and `virtualenv`, handling everything from installing dependencies to building and publishing the package.

If you're contributing to the project or running it locally for development, the steps below will help you set up your environment.

### 📥 Installing poetry

If necessary, install [poetry] according to the official [installation instructions](https://python-poetry.org/docs/#installation) 
(it's recommended to use [pipx](https://github.com/pypa/pipx) to install poetry in its own isolated environment but still have it available as a system wide command).

```shell
pip install pipx
pipx ensurepath
# reload your shell or start a new instance
pipx install poetry
```

### ⚙️ Configuring Poetry to Use an In-Project Virtual Environment (Optional)

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

### 📦 Installing dependencies

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

#### To PyPI

```shell
poetry build
poetry config repositories.pypi https://upload.pypi.org/legacy/
poetry config pypi-token.pypi your-token-here
poetry publish -r test-pypi
```

## Building the documentation

Documentation is generated using [Sphinx](https://www.sphinx-doc.org/), located in the `doc/` folder.

### With Poetry

```shell
poetry run sphinx-build -b html doc/ doc/_build/
```

### With Make

```shell
cd doc
make html
```
