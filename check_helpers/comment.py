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

    fmt_messages = ["* {commit} {message}".format(commit[:7], message) for commit, message in messages.keys()]

    all_comments = api.issue.list_comments(owner=os.getenv("GITHUB_REPOSITORY").split("/")[0],
                                           repo=os.getenv("GITHUB_REPOSITORY").split("/")[1],
                                           issue_number=pull_number)

    bad_comment = '''pr_sig_check report:

Please correct the following items: 
{}
'''.format("* ".join(fmt_messages))

    for comment in all_comments:

        if comment["body"].startswith("pr_sig_check report:"):
            # existing comments
            api.issue.update_comment(owner=os.getenv("GITHUB_REPOSITORY").split("/")[0],
                                     repo=os.getenv("GITHUB_REPOSITORY").split("/")[1],
                                     comment_id=comment["id"],
                                     body=bad_comment)
        else:
            api.issue.create_comment(owner=os.getenv("GITHUB_REPOSITORY").split("/")[0],
                                     repo=os.getenv("GITHUB_REPOSITORY").split("/")[1],
                                     issue_number=pull_number,
                                     body=bad_comment)
