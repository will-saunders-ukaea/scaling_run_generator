import sys
import os
import json
import itertools


class BaseSet:
    def __init__(self, template_name):
        self.template_name = template_name

class TaskSet(BaseSet):
    def __init__(self, task_set, template_name):
        super().__init__(template_name)
        self.task_set = task_set

class WeakScale(BaseSet):
    def __init__(self, base_name, scaling_factor, template_name):
        super().__init__(template_name)
        self.base_name = base_name
        self.scaling_factor = scaling_factor

    






