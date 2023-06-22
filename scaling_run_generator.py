import sys
import os
import json
import itertools
import importlib

from list_set import *


if __name__ == "__main__":

    config = json.loads(open(sys.argv[1]).read())
    print(config)

    print("=" * 80)


    iteration_set = config["iteration_set"]

    iteration_objs = [create_obj(dx) for dx in iteration_set]
    
    import pdb; pdb.set_trace()

    print("=" * 80)
    for ix in itertools.product(iteration_objs):

        print(ix)




    
    









