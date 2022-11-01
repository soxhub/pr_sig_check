#!/usr/bin/env python3

import logging

from ghapi.all import GhApi


class UserCheck:

    def __init__(self, author={}, orglist=[], domainlist=[], **kwargs):

        self.logger = logging.getLogger("UserCheck")

        self.api = GhApi()
        self.orglist = orglist
        self.domainlist = domainlist
        self.username = author.get("username", "unknown")
        self.email = author.get("email", "unknown")

        self.issue = False
        self.issues = list()

        if len(self.domainlist) > 0:
            self.check_domains()

        if len(self.orglist) > 0:
            self.check_orgs()

    def check_orgs(self):

        in_org = False

        for org in self.orglist:
            orgmatch = self.api.orgs.check_membership_for_user(org=org, username=self.username)

            self.logger.info(orgmatch)

    def check_domains(self):

        in_domain = False

        domain = self.email.split("@")

        if domain not in self.domainlist:
            # Failure
            self.issue = True
            self.issues.append("User's domain of {} not known {}".format(domain, ",".join(self.domainlist)))
        else:
            self.logger.info("User's domain of {} okay")
            pass




