#!/usr/bin/env python3

import os
import logging
from ghapi.all import GhApi
import git


def write_comment(is_failure=True, messages={}, pull_number=None, **kwargs):
    '''
    :param api: GHAPI Client
    :param is_failure: Write a failure Comment or a Success Comment
    :param messages: List of Markdown Messages to Include
    :param kwargs: Other Options
    :return:
    '''

    logger = logging.getLogger("write_comment")
    api = GhApi
    repo = git.Repo()

    print("Failure Messages: {}".format(messages))

    for commit, message in messages:
        files_changed = repo.git.diff(commit, name_only=True).split()

        all_comments = api.pulls.list_review_comments(owner=os.getenv("GITHUB_REPOSITORY").split("/")[0],
                                                      repo=os.getenv("GITHUB_REPOSITORY").split("/")[1],
                                                      pull_number=pull_number)

        bad_comment = '''pr_sig_check report:

Please correct the following items: 
{}

'''.format("* ".join(messages))

        '''found_comment = False

        for comment in all_comments:
            if comment["commit_id"] == commit:
                found_comment = True
                api.pulls.update_review_comment(owner=os.getenv("GITHUB_REPOSITORY").split("/")[0],
                                                repo=os.getenv("GITHUB_REPOSITORY").split("/")[1],
                                                comment_id=comment["id"],
                                                body=bad_comment)
        '''

        api.pull.create_review_comment(owner=os.getenv("GITHUB_REPOSITORY").split("/")[0],
                                       repo=os.getenv("GITHUB_REPOSITORY").split("/")[1],
                                       pull_number=pull_number,
                                       body=bad_comment,
                                       commit_id=commit,
                                       path=files_changed[0])
