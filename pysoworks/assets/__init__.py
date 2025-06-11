__all__ = [
    'get',
    'load_text'
]

import os
from typing import Union, List
from pathlib import Path
from PySide6.QtCore import QDir


ASSET_PATH = os.path.dirname(__file__)

QDir.addSearchPath('stylesheets', os.path.join(ASSET_PATH, 'stylesheets'))


def get(name: Union[str, Path, List[str]]) -> Path:
    if isinstance(name, list):
        name = os.path.join(*name)

    outpath = os.path.join(ASSET_PATH, name)
    if os.path.commonpath([outpath, ASSET_PATH]) != ASSET_PATH:
        raise RuntimeError("Directory traversal while reading an asset")
    return Path(outpath)


def load_text(name: Union[str, List[str]]) -> str:
    with open(get(name), 'r') as f:
        return f.read()



def load_stylesheet(name: str) -> str:
    if not name.endswith('.qss'):
        name += '.qss'
    return load_text(['stylesheets', name])
