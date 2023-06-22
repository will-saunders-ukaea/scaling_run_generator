import sys
import os
import json
import itertools
import importlib

from list_set import *
from run_management import *


if __name__ == "__main__":

    config = json.loads(open(sys.argv[1]).read())
    print(config)

    subs = get_subs(config)
    print(subs)

    for sx in subs:
        print(sx)

    create_run(config, subs)
