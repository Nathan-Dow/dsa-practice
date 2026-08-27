"""Sync accepted LeetCode submissions to this git repo.

Fetches your recent submissions from LeetCode, saves the latest accepted
solution per problem as <primary-tag>/<title-slug>.<ext> (the primary tag is
the first topic tag LeetCode lists for the problem), regenerates the README
index table, and commits + pushes each new or updated solution.

Setup:
  1. Log in to leetcode.com in your browser.
  2. Open DevTools (F12) -> Application -> Cookies -> https://leetcode.com
  3. Copy the value of the LEETCODE_SESSION cookie.
  4. Paste it into a file named .leetcode_session in this folder
     (the file is gitignored), or set the LEETCODE_SESSION env var.

Usage:
  python sync_leetcode.py            # sync and push
  python sync_leetcode.py --no-push  # commit locally only
"""

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.request
import urllib.error

REPO_DIR = os.path.dirname(os.path.abspath(__file__))
SESSION_FILE = os.path.join(REPO_DIR, ".leetcode_session")
CACHE_FILE = os.path.join(REPO_DIR, ".problem_cache.json")
README_FILE = os.path.join(REPO_DIR, "README.md")
API_URL = "https://leetcode.com/api/submissions/?offset={offset}&limit=20"
GRAPHQL_URL = "https://leetcode.com/graphql"
PAGE_DELAY_SECONDS = 1.5  # be polite to LeetCode between requests
MAX_PAGES = 15            # safety cap: 300 most recent submissions

EXTENSIONS = {
    "python": "py",
    "python3": "py",
    "cpp": "cpp",
    "c": "c",
    "java": "java",
    "csharp": "cs",
    "javascript": "js",
    "typescript": "ts",
    "golang": "go",
    "rust": "rs",
    "kotlin": "kt",
    "swift": "swift",
    "ruby": "rb",
    "scala": "scala",
    "php": "php",
    "dart": "dart",
    "racket": "rkt",
    "erlang": "erl",
    "elixir": "ex",
    "mysql": "sql",
    "mssql": "sql",
    "oraclesql": "sql",
    "postgresql": "sql",
}


def load_session():
    session = os.environ.get("LEETCODE_SESSION", "").strip()
    if not session and os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, encoding="utf-8") as f:
            session = f.read().strip()
    if not session:
        sys.exit(
            "No LeetCode session found.\n"
            "Put your LEETCODE_SESSION cookie value in a file named "
            f"{os.path.basename(SESSION_FILE)!r} in this folder,\n"
            "or set the LEETCODE_SESSION environment variable.\n"
            "(Browser: F12 -> Application -> Cookies -> leetcode.com -> LEETCODE_SESSION)"
        )
    return session


def fetch_page(session, offset):
    req = urllib.request.Request(
        API_URL.format(offset=offset),
        headers={
            "Cookie": f"LEETCODE_SESSION={session}",
            "Referer": "https://leetcode.com/",
            "User-Agent": "Mozilla/5.0",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        if e.code in (401, 403):
            sys.exit(
                "LeetCode rejected the session cookie (it likely expired).\n"
                "Grab a fresh LEETCODE_SESSION value from your browser and update "
                f"{os.path.basename(SESSION_FILE)!r}."
            )
        raise


def fetch_accepted_solutions(session):
    """Return {title_slug: submission_dict} with the newest accepted run per problem."""
    solutions = {}
    offset = 0
    for _ in range(MAX_PAGES):
        data = fetch_page(session, offset)
        submissions = data.get("submissions_dump", [])
        for sub in submissions:
            if sub.get("status_display") != "Accepted":
                continue
            slug = sub["title_slug"]
            # Submissions come newest-first, so keep the first one we see.
            if slug not in solutions:
                solutions[slug] = sub
        if not data.get("has_next") or not submissions:
            break
        offset += len(submissions)
        time.sleep(PAGE_DELAY_SECONDS)
    return solutions


def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_cache(cache):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2)


def fetch_problem_meta(slug):
    """Fetch number, title, difficulty, and topic tags (public data, no auth)."""
    payload = json.dumps({
        "query": (
            "query q($slug: String!) { question(titleSlug: $slug) {"
            " questionFrontendId title difficulty topicTags { name slug } } }"
        ),
        "variables": {"slug": slug},
    }).encode("utf-8")
    req = urllib.request.Request(
        GRAPHQL_URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Referer": f"https://leetcode.com/problems/{slug}/",
            "User-Agent": "Mozilla/5.0",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        question = json.loads(resp.read().decode("utf-8"))["data"]["question"]
    if question is None:
        return None
    return {
        "id": question["questionFrontendId"],
        "title": question["title"],
        "difficulty": question["difficulty"],
        "tags": [t["name"] for t in question["topicTags"]],
        "primary_tag": (
            question["topicTags"][0]["slug"] if question["topicTags"] else "misc"
        ),
    }


def get_problem_meta(slug, cache):
    if slug not in cache:
        meta = fetch_problem_meta(slug)
        if meta is None:
            meta = {
                "id": "?", "title": slug, "difficulty": "?",
                "tags": [], "primary_tag": "misc",
            }
        cache[slug] = meta
        save_cache(cache)
        time.sleep(PAGE_DELAY_SECONDS)
    return cache[slug]


def build_readme(cache, filenames):
    """Render the index table for every problem that has a solution file."""
    lines = [
        "# DSA Practice",
        "",
        "My accepted LeetCode solutions, synced automatically by "
        "[`sync_leetcode.py`](sync_leetcode.py). Folders are each problem's "
        "primary topic tag.",
        "",
        "| # | Problem | Difficulty | Tags | Solution |",
        "|--:|---------|------------|------|----------|",
    ]
    def sort_key(slug):
        pid = cache[slug]["id"]
        return (0, int(pid)) if pid.isdigit() else (1, 0)
    for slug in sorted(filenames, key=sort_key):
        meta = cache[slug]
        rel_path = filenames[slug].replace(os.sep, "/")
        lines.append(
            f"| {meta['id']} "
            f"| [{meta['title']}](https://leetcode.com/problems/{slug}/) "
            f"| {meta['difficulty']} "
            f"| {', '.join(meta['tags'])} "
            f"| [{os.path.basename(rel_path)}]({rel_path}) |"
        )
    return "\n".join(lines) + "\n"


def run_git(*args):
    result = subprocess.run(
        ["git", *args], cwd=REPO_DIR, capture_output=True, text=True
    )
    if result.returncode != 0:
        sys.exit(f"git {' '.join(args)} failed:\n{result.stderr.strip()}")
    return result.stdout.strip()


def commit_if_staged_changes(paths, message):
    run_git("add", *paths)
    if run_git("status", "--porcelain", "--", *paths):
        run_git("commit", "-m", message)
        print(f"Committed: {message}")
        return True
    return False


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--no-push", action="store_true", help="commit but don't push")
    args = parser.parse_args()

    session = load_session()
    cache = load_cache()
    print("Fetching submissions from LeetCode...")
    solutions = fetch_accepted_solutions(session)
    if not solutions:
        print("No accepted submissions found.")
        return

    committed = 0
    filenames = {}  # slug -> repo-relative solution path, for the README
    for slug, sub in sorted(solutions.items(), key=lambda kv: kv[1]["timestamp"]):
        meta = get_problem_meta(slug, cache)
        ext = EXTENSIONS.get(sub["lang"], "txt")
        rel_path = os.path.join(meta["primary_tag"], f"{slug}.{ext}")
        filenames[slug] = rel_path
        path = os.path.join(REPO_DIR, rel_path)
        code = sub["code"].replace("\r\n", "\n")
        if not code.endswith("\n"):
            code += "\n"

        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                if f.read() == code:
                    continue  # already up to date
            message = f"feat: update {slug}"
        else:
            message = f"feat: {slug}"

        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(code)
        commit_paths = [rel_path]
        # Migrate a pre-folder copy of this solution from the repo root.
        old_root_file = os.path.join(REPO_DIR, f"{slug}.{ext}")
        if os.path.exists(old_root_file):
            os.remove(old_root_file)
            commit_paths.append(f"{slug}.{ext}")
        if commit_if_staged_changes(commit_paths, message):
            committed += 1

    readme = build_readme(cache, filenames)
    with open(README_FILE, "w", encoding="utf-8", newline="\n") as f:
        f.write(readme)
    if commit_if_staged_changes(["README.md"], "docs: update solution index"):
        committed += 1

    if committed == 0:
        print("Everything already up to date.")
        return

    if args.no_push:
        print(f"{committed} commit(s) created (not pushed).")
    else:
        print("Pushing to GitHub...")
        run_git("push")
        print(f"Done - {committed} commit(s) uploaded.")


if __name__ == "__main__":
    main()
