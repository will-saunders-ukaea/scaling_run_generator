import sys
import os
import json
import math
import importlib


class Machine:
    def __init__(self, config):
        self.config = config["machine"]
        self.num_tasks_per_node = int(self.config["tasks_per_node"])
        self.mpirun = self.config.get(
            "mpirun", "mpirun -n {NUM_TASKS} {EXECUTABLE} {ARGS}"
        )


def group_by_node(machine, subs):
    nd = {}
    for sub in subs:
        num_nodes = int(math.ceil(sub["NUM_TASKS"] / machine.num_tasks_per_node))
        if not num_nodes in nd.keys():
            nd[num_nodes] = list()
        nd[num_nodes].append(sub)
    return nd


def get_args(config, subdir, subs):

    filetypes = importlib.import_module("filetypes")

    file_objs = []
    for arg in config["templates"]["input_args"]:
        fx_type = arg[0]
        fx_file = arg[1]
        fx_obj = getattr(filetypes, fx_type)(fx_file)
        fx_obj.process(subs, subdir)
        file_objs.append(fx_obj.get_arg(subdir))

    return " ".join(file_objs)


def create_node_dir(config, num_tasks, subs):
    basedir = os.path.join(config["directory"], f"nodes_{num_tasks}")
    os.makedirs(basedir)

    launch_dir_cmd = []
    for subi, sub in enumerate(subs):
        subdir = os.path.join(basedir, f"run_{subi}")
        os.makedirs(subdir)
        args = get_args(config, subdir, sub)
        launch_dir_cmd.append((str(sub["NUM_TASKS"]), os.path.abspath(subdir), args))
        with open(os.path.join(subdir, "config.json"), "w") as fh:
            fh.write(json.dumps(sub, indent=2))

    return basedir, launch_dir_cmd


def create_jobscript(num_nodes, config, machine, directory, launch_dir_cmd):
    jobscript = open(config["templates"]["jobscript"]).read()

    jobscript = jobscript.replace("{{NUM_NODES}}", str(num_nodes))
    num_tasks = num_nodes * machine.num_tasks_per_node
    jobscript = jobscript.replace("{{NUM_TASKS}}", str(num_tasks))
    jobscript = jobscript.replace("{{NUM_TASKS_PER_NODE}}",
        str(machine.num_tasks_per_node))

    cmds = ""
    for cmd in launch_dir_cmd:
        cmds += "cd {}\n".format(cmd[1])
        ARGS = cmds[2]
        EXECUTABLE = config["executable"]
        cmds += (
            machine.mpirun.format(NUM_TASKS=cmd[0], EXECUTABLE=EXECUTABLE, ARGS=cmd[2])
            + " | tee stdout\n"
        )
    jobscript = jobscript.replace("{{LAUNCH_CMDS}}", cmds)

    with open(os.path.join(directory, "jobscript"), "w") as fh:
        fh.write(jobscript)


def create_run(config, subs):

    machine = Machine(config)
    subs = group_by_node(machine, subs)

    for sx in subs.items():
        directory, launch_dir_cmd = create_node_dir(config, sx[0], sx[1])
        create_jobscript(
            sx[0],
            config,
            machine,
            directory,
            launch_dir_cmd,
        )

    with open(os.path.join(config["directory"], "config.json"), "w") as fh:
        fh.write(json.dumps(config, indent=2))
