#!/usr/bin/env python3

import os
import logging
from ghapi.all import GhApi
from github import Github
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
    api = GhApi()
    pyapi = Github()
    repo = git.Repo()

    print("Failure Messages: {}".format(messages))

    fmt_messages = ["* {commit} {message}".format(commit=commit[:7], message=message) for commit, message in messages.items()]

    repo = pyapi.get_repo(os.getenv("GITHUB_REPOSITORY"))
    pr = repo.get_pull(pull_number)

    print("Making a test comment")
    pr.create_issue_comment("This is a Test")
    print("Test Comment Made")

    all_comments = pr.get_issue_comments()

    bad_comment = '''pr_sig_check report:

Please correct the following items: 
{}
'''.format("* ".join(fmt_messages))

    print("Wanted Comment: \n{}".format(bad_comment))

    for comment in all_comments:

        if comment.body.startswith("pr_sig_check report:"):
            comment.delete()

    print("Found No existing comment, creating a new one.")
    try:
        pr.create_issue_comment(body=bad_comment)
    except Exception as error:
        print("Unable to Comment on PR {}".format(error))
