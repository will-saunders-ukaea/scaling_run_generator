import sys
import os
import json
import itertools
import importlib

from base_iteration_types import BaseIterationSet

class ListSet(BaseIterationSet):
    def __init__(self, list_set):
        super().__init__()
        base_types = importlib.import_module("base_iteration_types")
        for lx in list_set["list_set"]:
            obj_name = lx["type"]
            self.mods.append(
                getattr(base_types, obj_name)(**lx["parameters"])
            )

def create_obj(d):
    if d["type"] == "ListSet":
        return ListSet(d["parameters"])
    else:
        base_types = importlib.import_module("base_iteration_types")
        return getattr(base_types, d["type"])(**d["parameters"])


def get_subs(config):

    iteration_set = config["iteration_set"]
    iteration_objs = [create_obj(dx).get() for dx in iteration_set]
    
    subs_list = []
    for mods in itertools.product(*iteration_objs):
        subs = {}
        for mod in mods:
            mod.update(subs)
        subs_list.append(subs)

    return subs_list


