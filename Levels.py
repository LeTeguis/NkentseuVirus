#!/usr/bin/python3
import sys
import importlib
import shutil
import os
from pathlib import Path

levels_infos = []
levels_actual = 0


def download_algorithme(path):
    filepath = Path(path)
    dst = f"ia/{filepath.name}"
    shutil.copy(path, dst)

    importe_algorithme(filepath.name.rsplit(".py", 0))


def importe_algorithme(algo_name):
    module = importlib.import_module(algo_name, "ia")
    algorithme = getattr(module, algo_name)()
    levels_infos.append(algorithme)

    return 0


levels_actual = importe_algorithme("FirstIA")
