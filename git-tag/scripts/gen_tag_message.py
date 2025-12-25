#!/usr/bin/env python3
import argparse
import re
import subprocess
import sys

ORDER = [
    "Breaking Changes",
    "Features",
    "Fixes",
    "Performance",
    "Refactor",
    "Docs",
    "Tests",
    "Build",
    "CI",
    "Chore",
    "Other",
]

TYPE_MAP = {
    "feat": "Features",
    "feature": "Features",
    "fix": "Fixes",
    "perf": "Performance",
    "refactor": "Refactor",
    "docs": "Docs",
    "test": "Tests",
    "build": "Build",
    "ci": "CI",
    "chore": "Chore",
}


def run_git(args):
    result = subprocess.run(["git"] + args, text=True, capture_output=True)
    if result.returncode != 0:
        err = result.stderr.strip() or result.stdout.strip()
        raise RuntimeError(err or "git command failed")
    return result.stdout


def try_git(args):
    try:
        return run_git(args)
    except RuntimeError:
        return ""


def get_last_tag():
    out = try_git(["describe", "--tags", "--abbrev=0"]).strip()
    if out:
        return out
    out = try_git(["tag", "--sort=-creatordate"]).strip()
    if out:
        return out.splitlines()[0].strip()
    return ""


def get_commits(range_spec, max_count):
    cmd = ["log", "--pretty=format:%h%x09%s"]
    if max_count is not None:
        cmd += ["--max-count", str(max_count)]
    if range_spec:
        cmd.append(range_spec)
    out = run_git(cmd).strip()
    commits = []
    if not out:
        return commits
    for line in out.splitlines():
        if not line.strip():
            continue
        if "\t" in line:
            commit_hash, subject = line.split("\t", 1)
        else:
            parts = line.split(" ", 1)
            commit_hash = parts[0]
            subject = parts[1] if len(parts) > 1 else ""
        commits.append((commit_hash.strip(), subject.strip()))
    return commits


def classify_subject(subject):
    text = subject.strip()
    lower = text.lower()

    is_breaking = "breaking" in lower
    m = re.match(r"([a-zA-Z]+)(\([^)]*\))?(!)?:", text)
    if m:
        ctype = m.group(1).lower()
        if m.group(3):
            is_breaking = True
        if is_breaking:
            return "Breaking Changes"
        return TYPE_MAP.get(ctype, "Other")

    for key, label in TYPE_MAP.items():
        if lower.startswith(key):
            return label

    if is_breaking:
        return "Breaking Changes"

    return "Other"


def build_message(tag, commits):
    title = f"Release {tag}" if tag else "Release"
    if not commits:
        return f"{title}\n\nNo changes."

    grouped = {name: [] for name in ORDER}
    for commit_hash, subject in commits:
        label = classify_subject(subject)
        grouped[label].append(f"- {subject} ({commit_hash})")

    lines = [title, ""]
    for name in ORDER:
        items = grouped[name]
        if not items:
            continue
        lines.append(name)
        lines.extend(items)
        lines.append("")

    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate git tag message from git log")
    parser.add_argument("--tag", help="Tag name to include in the title")
    parser.add_argument("--since-tag", help="Use a specific tag as the log base")
    parser.add_argument("--max", type=int, help="Limit number of commits")
    parser.add_argument("--output", help="Write message to a file")
    args = parser.parse_args()

    try:
        run_git(["rev-parse", "--is-inside-work-tree"])
    except RuntimeError as exc:
        print(f"Not a git repository: {exc}", file=sys.stderr)
        return 1

    base_tag = args.since_tag or get_last_tag()
    range_spec = f"{base_tag}..HEAD" if base_tag else ""

    try:
        commits = get_commits(range_spec, args.max)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    message = build_message(args.tag, commits)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(message)
            handle.write("\n")
    else:
        print(message)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
