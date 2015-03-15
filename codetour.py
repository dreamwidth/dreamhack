"""Generate a code tour from a repository given a time span"""

from datetime import datetime
import re
import requests
from collections import defaultdict

ISSUE_NUMBER_RE = re.compile(r'#(\d+)')

def fetch_from_repo(repo, since):
    """Fetch list of issues from a given repo."""
    req = requests.get("https://api.github.com/repos/%s/issues" % repo,
                       params={"state": "closed",
                               "sort": "updated",
                               "since": "%sZ" % since.isoformat()
                              })
    issues = req.json()

    old_req = None
    while old_req != req:
        old_req = req

        if "link" in req.headers:
            print req.headers["link"]
            for link in req.headers["link"].split(","):
                match = re.search('<([^>]+)>; rel="next"', link)
                if match:
                    url = match.group(1)
                    req = requests.get(url)
                    issues.extend(req.json())

    return issues


def fetch_issues(since_input):
    """Fetch issues from github for a given timespan."""
    since = datetime.strptime(since_input, "%Y-%m-%d")

    dw_free = fetch_from_repo("dreamwidth/dw-free", since)
    dw_nonfree = fetch_from_repo("dreamwidth/dw-nonfree", since)
    for issue in dw_nonfree:
        issue["is_nonfree"] = True

    issues = dw_free
    issues.extend(dw_nonfree)

    return issues

def extract_data(raw_data):
    """Extracts the values that we need from the raw data and returns a list.
       Each item contain: 'category', 'assignee', 'pr_url', 'issue_url', 'title'
       Also merges pull request data into its associated issue data
    """

    # list of (issue, pull_request, nonfree_pull_request) data
    grouped_issues = defaultdict(dict)
    for item in raw_data:
        issue_number = str(item["number"])

        title = item["title"]
        is_pull_request = False

        if "pull_request" in item:
            match = re.search(ISSUE_NUMBER_RE, "%s%s" % (title, item["body"]))

            if match:
                # use the issue's number instead of our own
                issue_number = match.group(1)
                is_pull_request = True

        issue = {
            "title" : title,
            "number": issue_number,
        }

        issue["issue_url"] = item["html_url"]
        if item["assignee"]:
            issue["assignee"] = item["assignee"]["login"]

        if "pull_request" in item:
            if "is_nonfree" in item:
                issue["pr_nonfree_url"] = issue["pr_url"] = item["pull_request"]["html_url"]
            else:
                issue["pr_url"] = item["pull_request"]["html_url"]
            issue["assignee"] = item["user"]["login"]

        if item["milestone"]:
            issue["category"] = item["milestone"]["title"]

        if is_pull_request:
            if "is_nonfree" in item:
                grouped_issues[issue_number]["pr_nonfree"] = issue
            else:
                grouped_issues[issue_number]["pr"] = issue
        else:
            grouped_issues[issue_number]["issue"] = issue

    issues = []
    for i in sorted(grouped_issues, key=int):
        issue = grouped_issues[i]
        final = {}
        final.update(issue.get("pr_nonfree", {}))
        final.update(issue.get("pr", {}))
        final.update(issue.get("issue", {}))
        issues.append(final)

    return issues

def github_tag(username):
    """Returns the github user markup given a username."""
    return "<user name='%s' site='github.com'>" % username

def print_codetour(issues):
    """Print out the code tour."""

    text = []
    contributors = set()

    for issue in issues:
        pr_link = " (<a href='%s'>pull request</a>)" % issue["pr_url"] if "pr_url" in issue else ""
        pr_nonfree_link = " (<a href='%s'>nonfree pull request</a>)" % issue["pr_nonfree_url"] if "pr_nonfree_url" in issue else ""
        text.append("<b><a href='%s'>Issue %s</a>:</b> %s%s%s" %
                    (issue["issue_url"], issue["number"], issue["title"], pr_link, pr_nonfree_link))

        github_link = ""
        if "assignee" in issue:
            github_link = github_tag(issue["assignee"])
            contributors.add(issue["assignee"])

        text.append("<b>Category:</b> %s" % issue.get("category", ""))
        text.append("<b>Patch by:</b> %s" % github_link)
        text.append("<b>Description:</b> FILL IN")
        text.append("")

    # summary
    contributors_list = [github_tag(s) for s in sorted(contributors)]
    text.append("")
    text.append("%d total issues resolved" % len(issues))
    text.append("Contributors: %s" % ', '.join(contributors_list))

    print '\n'.join(text)


if __name__ == '__main__':
    codetour_issues = extract_data(fetch_issues("2015-01-17"))
    print_codetour(codetour_issues)
