#!/usr/bin/env python3

import argparse
import logging
import os
import sys
import subprocess
from ghapi.all import GhApi

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

# for currentpath, folders, files in os.walk(_workdir):
#    for this_file in files:
#        this_abs_file = "{}/{}".format(currentpath, this_file)
#        print(this_abs_file)

env_cmds = '''
echo GITHUB_REF : ${GITHUB_REF} ; 
echo GITHUB_REF_NAME : ${GITHUB_REF_NAME} ;
echo GITHUB_BASE_REF : ${GITHUB_BASE_REF} ; 
echo GITHUB_HEAD_REF : ${GITHUB_HEAD_REF} ; 
echo GITHUB_EVENT_NAME : ${GITHUB_EVENT_NAME} ;
echo GITHUB_REPOSITORY_OWNER : ${GITHUB_REPOSITORY_OWNER} ;
echo GITHUB_REPOSITORY : ${GITHUB_REPOSITORY} ;
'''

log_cmd = subprocess.run("git log", shell=True, capture_output=True)
print(log_cmd.stdout.decode())

env_cmd = subprocess.run(env_cmds, shell=True, capture_output=True)
print(env_cmd.stdout.decode())
# set token here
api = GhApi()

if os.getenv("GITHUB_EVENT_NAME") != "pull_request":
    logger.error("Non-Pull Requests not Yet Supported")
    sys.exit(1)

pull_number = os.getenv("GITHUB_REF").split("/")[2]

iteration = 0
continue_iteration = True
all_commits = list()

while continue_iteration is True:
    logger.debug("Getting Page {} of Results.".format(iteration))

    these_commits = api.pulls.list_commits(owner=os.getenv("GITHUB_REPOSITORY").split("/")[0],
                                           repo=os.getenv("GITHUB_REPOSITORY").split("/")[1],
                                           pull_number=pull_number,
                                           per_page=50,
                                           iteration=iteration)

    all_commits.extend(these_commits)

    if len(these_commits) < 50:
        continue_iteration = False

failures_commits = 0

for commit in all_commits:
    if commit["commit"]["verification"] is True:
        # Valid Commit
        print("Commit {} is Validated by Github.".format(commit["sha"][:7]))
    else:
        print("Commit {} is Unvalidated by Github.".format(commit["sha"][:7]))
        print(commit)
        failures_commits += 1

    # Organization Checks Here in Future

if failures_commits > 0:
    # Future Comment Back to Pull request logic
    print("There are {} unsigned commits in this pull request.".format(failures_commits))
    sys.exit(1)
else:
    print("Check passed all commits are properly signed.")
    sys.exit(0)