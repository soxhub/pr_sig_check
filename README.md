# pr_sig_check

A GH Action to Check the commits of a pull request to see if they're signed.

Example Check:

```
# Check Commits
name: PR Commit Signed Check

# Controls when the action will run. Triggers the workflow on push or pull request
# events but only for the master branch
on:
  pull_request:
    branches:
      - main
      - master
      - develop

jobs:
  check_commits:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Checks Commits Signing
        uses: soxhub/pr_sig_check@v1.0.4
        with:
          domaincheck: "domaina.com,domainb.com"
          orgcheck: "myorg"
        env:
          GITHUB_TOKEN: ${{ github.token }}
```

Please note that orgcheck can only confirm **public** members at this time. Additionally, there's an option `notifyonly: yes`
that can be set in the with to make it so that the check just comments on pulls and doesn't fail builds.
