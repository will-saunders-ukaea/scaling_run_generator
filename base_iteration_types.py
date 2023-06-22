import sys
import os
import json
import itertools


class BaseTemplateModifier:
    def __init__(self, template_name):
        self.template_name = template_name

    def update(self, subs):
        pass


class BaseIterationSet:
    def __init__(self):
        self.mods = []

    def get(self):
        return self.mods


class WeakScale(BaseTemplateModifier):
    def __init__(self, base_name, scaling_factor, template_name):
        super().__init__(template_name)
        self.base_name = base_name
        self.scaling_factor = scaling_factor

    def update(self, subs):
        subs[self.template_name] = int(subs[self.base_name]) * self.scaling_factor


class NumTasks(BaseTemplateModifier):
    def __init__(self, num_tasks, template_name):
        super().__init__(template_name)
        self.num_tasks = num_tasks

    def update(self, subs):
        subs[self.template_name] = self.num_tasks


class TaskSet(BaseIterationSet):
    def __init__(self, task_set, template_name):
        super().__init__()
        self.template_name = template_name
        self.task_set = task_set
        for tx in task_set:
            self.mods.append(NumTasks(tx, template_name))
