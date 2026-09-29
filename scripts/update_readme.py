#!/usr/bin/env python3
"""Regenerate the auto-managed section of README.md from live GitHub data.

Finds every pull request the profile owner has opened against repositories
they do not own, groups them by project, marks each one with its status
(merged, approved, changes requested, in review, draft, closed) and rewrites
the block between the <!-- CONTRIBUTIONS:START/END --> markers in README.md.

Project names and one-line summaries come from projects.json; a project
missing from that file falls back to its repository name and description.

Only the standard library is used. Needs a token in GITHUB_TOKEN (the
default Actions token is enough, since only public data is read).
"""

import datetime
import json
import os
import pathlib
import re
import sys
import urllib.request

USER = os.environ.get("PROFILE_USER", "Abtektas")
ROOT = pathlib.Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
PROJECTS = ROOT / "projects.json"

QUERY = """
query($q: String!, $cursor: String) {
  search(query: $q, type: ISSUE, first: 100, after: $cursor) {
    pageInfo { hasNextPage endCursor }
    nodes {
      ... on PullRequest {
        number title url state isDraft merged mergedAt createdAt closedAt
        reviewDecision
        repository { nameWithOwner name url description }
      }
    }
  }
}
"""

# Icon and label for each status, in summary order.
STATUSES = {
    "merged": ("✅", "merged"),
    "approved": ("👍", "approved"),
    "changes": ("🔁", "changes requested"),
    "review": ("⏳", "in review"),
    "draft": ("📝", "draft"),
    "closed": ("✖️", "closed"),
}

UPDATED_RE = re.compile(r"^<sub>Last updated .*</sub>$", re.M)


def graphql(query, variables):
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        sys.exit("GITHUB_TOKEN is not set")
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={"Authorization": f"bearer {token}", "User-Agent": USER},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = json.load(resp)
    if body.get("errors"):
        sys.exit(f"GraphQL error: {body['errors']}")
    return body["data"]


def fetch_pull_requests():
    q = f"is:pr author:{USER} -user:{USER} sort:created-desc"
    prs, cursor = [], None
    while True:
        search = graphql(QUERY, {"q": q, "cursor": cursor})["search"]
        prs += [n for n in search["nodes"] if n]
        if not search["pageInfo"]["hasNextPage"]:
            return prs
        cursor = search["pageInfo"]["endCursor"]


def status_of(pr):
    if pr["merged"]:
        return "merged"
    if pr["state"] == "CLOSED":
        return "closed"
    if pr["isDraft"]:
        return "draft"
    if pr["reviewDecision"] == "APPROVED":
        return "approved"
    if pr["reviewDecision"] == "CHANGES_REQUESTED":
        return "changes"
    return "review"


def fmt_date(iso):
    return datetime.date.fromisoformat(iso[:10]).strftime("%b %-d, %Y")


def escape(text):
    return text.replace("[", "\\[").replace("]", "\\]").replace("<", "&lt;")


def summarize(prs):
    counts = {}
    for pr in prs:
        counts[status_of(pr)] = counts.get(status_of(pr), 0) + 1
    return " · ".join(
        f"{icon} {counts[key]} {label}"
        for key, (icon, label) in STATUSES.items()
        if key in counts
    )


def render_pr(pr):
    status = status_of(pr)
    icon, label = STATUSES[status]
    if status == "merged":
        when = f"merged {fmt_date(pr['mergedAt'])}"
    elif status == "closed":
        when = f"closed {fmt_date(pr['closedAt'])}"
    else:
        when = f"{label}, opened {fmt_date(pr['createdAt'])}"
    return f"- {icon} [{escape(pr['title'])}]({pr['url']}) <sub>{when}</sub>"


def render(prs, projects):
    if not prs:
        return "_No upstream pull requests yet._"

    by_repo = {}
    for pr in prs:  # already newest first, so projects end up by latest activity
        by_repo.setdefault(pr["repository"]["nameWithOwner"], []).append(pr)

    out = [
        f"**{len(prs)}** pull requests to **{len(by_repo)}** projects"
        f" · {summarize(prs)}",
    ]
    for full_name, items in by_repo.items():
        repo = items[0]["repository"]
        meta = projects.get(full_name, {})
        name = meta.get("name", repo["name"])
        summary = meta.get("summary") or repo["description"] or ""
        out += ["", f"#### [{name}]({repo['url']})"]
        if summary:
            out += [summary, ""]
        out += [render_pr(pr) for pr in items]
    return "\n".join(out)


def main():
    projects = json.loads(PROJECTS.read_text()) if PROJECTS.exists() else {}
    body = render(fetch_pull_requests(), projects)

    original = README.read_text()
    pattern = re.compile(
        r"(<!-- CONTRIBUTIONS:START -->\n).*?(<!-- CONTRIBUTIONS:END -->)", re.S
    )
    if not pattern.search(original):
        sys.exit("README.md is missing the CONTRIBUTIONS markers")
    updated = pattern.sub(lambda m: m.group(1) + body + "\n" + m.group(2), original)

    # Only touch the timestamp when the data actually changed, so scheduled
    # runs with nothing new don't produce a commit.
    if UPDATED_RE.sub("", updated) == UPDATED_RE.sub("", original):
        print("No changes.")
        return
    today = datetime.datetime.now(datetime.timezone.utc).strftime("%b %-d, %Y")
    updated = UPDATED_RE.sub(
        f"<sub>Last updated {today} by "
        f"[GitHub Actions](.github/workflows/update-readme.yml)</sub>",
        updated,
    )
    README.write_text(updated)
    print("README.md updated.")


if __name__ == "__main__":
    main()
