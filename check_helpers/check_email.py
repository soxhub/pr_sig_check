#!/usr/bin/env python3

import logging

from ghapi.all import GhApi


class UserCheck:

    def __init__(self, commit={}, orglist=[], domainlist=[], **kwargs):

        self.logger = logging.getLogger("UserCheck")

        self.api = GhApi()
        self.orglist = orglist
        self.domainlist = domainlist
        self.commit = commit

        self.issue = False
        self.issues = list()

        if len(self.domainlist) > 0:
            self.check_domains()

        if len(self.orglist) > 0:
            self.check_orgs()

    def check_orgs(self):

        in_org = False
        username = self.commit["author"].get("login")

        for org in self.orglist:
            try:
                self.api.orgs.check_membership_for_user(org=org, username=username)
            except Exception as not_in_error:
                self.logger.error("User not in the organization: {}".format(not_in_error))
            else:
                # User is in this Org
                in_org = True

        if in_org is False:
            self.issue = True
            self.issues.append("User {} is not in any of the following organizations : {}".format(username, ", ".join(self.orglist)))


    def check_domains(self):

        in_domain = False

        email = self.commit["commit"]["author"]["email"]

        domain = email.split("@")[1]

        if domain not in self.domainlist:
            # Failure
            self.issue = True
            self.issues.append("User {} domain of {} not known {}".format(email, domain, ", ".join(self.domainlist)))
        else:
            self.logger.info("User {} domain of {} okay".format(email, domain, ", ".join(self.domainlist)))
            pass




