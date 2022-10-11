#!/usr/bin/env python3

import argparse
import logging
import os
import sys
import subprocess

_workdir = "/github/workspace"


if __name__ == "__main__":

    """
    Let's grab my runtime options
    """

    parser = argparse.ArgumentParser()

    parser.add_argument("-v", "--verbose", action="append_const", help="Verbosity Controls",
                        const=1, default=[])

    args = parser.parse_args()

    VERBOSE = len(args.verbose)

    if VERBOSE == 0:
        logging.basicConfig(level=logging.ERROR)
    elif VERBOSE == 1:
        logging.basicConfig(level=logging.WARNING)
    elif VERBOSE == 2:
        logging.basicConfig(level=logging.INFO)
    elif VERBOSE > 2:
        logging.basicConfig(level=logging.DEBUG)

    logger = logging.getLogger("check_commits")


for currentpath, folders, files in os.walk(_workdir):
    for this_file in files:
        this_abs_file = "{}/{}".format(currentpath, this_file)
        print(this_abs_file)


log_cmd = subprocess.run("git log", shell=True, capture_output=True)

print(log_cmd.stdout)

