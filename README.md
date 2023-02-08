# pr_sig_check

A GH Action to Check the commits of a pull request to see if they're signed. As long as Github believes the commit is
signed with a gpg or other key this system will see it as signed. This tool **will not** introspect into Github signed
actions (like pull requests or browser based commits) to see if the consistent pieces are signed. So keep that in mind
when choosing which pulls to evaluate.

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
        uses: soxhub/pr_sig_check@v1.0.6
        with:
          domaincheck: "domaina.com,domainb.com"
          orgcheck: "myorg"
        env:
          GITHUB_TOKEN: ${{ github.token }}
```

## Options

### `orgcheck`

Org check can check to make sure that contributors are part of your public github organization. Please note that 
orgcheck can only confirm **public** members at this time. Format orgs as a comma seperated list for multiple orgs
(eg: `org1,org2,org3`)

### `notifyonly`

Additionally, there's an option `notifyonly` instead of "breaking the build" this will always pass. It will just comment
on the pull request and not break the build. This is useful if you're trying to begin a program of commit signing at 
your organization.

### `domaincheck`

Domain check will check the email domain of the user makign the commit. You can restrict emails to particular domains.
This is especially useful if your organization's membership is not public. Remember that you can add multiple domains by
comma seperating the list (eg: `domain.com,domain.org,otherdomain.com`)

### `verbose`

Verbosity as a number with higher numbers representing more verbosity (maximum is 4 all numbers beyond that are 4). This
increases the verbosity of the logs in the github action log file. Useful when debugging.

### `customurl`

In addition to [Github's Signing Documentation](https://docs.github.com/en/authentication/managing-commit-signature-verification/signing-commits)
you can add a custom url to be included in any error messages. URLs should be comma seperated and you can optionally semicolon
seperate each sub option with `label;url` if that helps. So you could do something like this: 
`Internal Wiki;https://ourwiki.com/path/to/doc,Another Doc;https://blah.com/path/to/other/doc`. Failure messages will
include these documents in its failure messages to guide your users.
