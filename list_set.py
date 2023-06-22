import sys
import os
import json
import itertools
import importlib

class ListSet:
    def __init__(self, list_set):
        base_types = importlib.import_module("base_iteration_types")
        self.objs = []
        for lx in list_set["list_set"]:
            obj_name = lx["type"]
            self.objs.append(
                getattr(base_types, obj_name)(**lx["parameters"])
            )


def create_obj(d):
    if d["type"] == "ListSet":
        return ListSet(d["parameters"])
    else:
        base_types = importlib.import_module("base_iteration_types")
        return getattr(base_types, d["type"])(**d["parameters"])

