import operator
import logging
from functools import reduce
from itertools import chain
from urllib.parse import urlparse
import requests
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class GitError(Exception):
    pass


def _get_from_dict(dataDict, mapList):
    """Access a nested dictionary using a list of keys."""
    return reduce(operator.getitem, mapList, dataDict)


def _append_in_dict(dataDict, mapList, value):
    """Append a value to a list in a nested dictionary."""
    _get_from_dict(dataDict, mapList[:-2])[mapList[-2]].append(value)


def _get_sha(author, repo):
    """Get the SHA of the master branch."""
    url = f'https://api.github.com/repos/{author}/{repo}/branches/master'
    response = requests.get(url)
    while response.status_code == 403:  # Rate limit exceeded
        reset_time = int(response.headers.get("X-RateLimit-Reset"))
        sleep_time = max(0, reset_time - time.time())
        logging.info(f"Rate limited. Sleeping for {sleep_time} seconds.")
        time.sleep(sleep_time)
        response = requests.get(url)
    if response.status_code != 200:
        raise GitError(f"Invalid author or repo name: {response.status_code}")
    try:
        return response.json()['commit']['commit']['tree']['sha']
    except KeyError as ex:
        raise GitError("Unexpected response format") from ex


def _get_git_tree(author, repo, sha):
    """Get the git tree using the SHA."""
    url = f"https://api.github.com/repos/{author}/{repo}/git/trees/{sha}?recursive=1"
    response = requests.get(url)
    while response.status_code == 403:  # Rate limit exceeded
        reset_time = int(response.headers.get("X-RateLimit-Reset"))
        sleep_time = max(0, reset_time - time.time())
        logging.info(f"Rate limited. Sleeping for {sleep_time} seconds.")
        time.sleep(sleep_time)
        response = requests.get(url)
    if response.status_code != 200:
        raise GitError(f"Failed to get git tree: {response.status_code}")
    return response.json().get("tree", [])


def git_tree(repostring):
    """Generate a nested dictionary representing the file structure of a GitHub repo."""
    author, repo = repostring.split("/")
    sha = _get_sha(author, repo)
    tree = {repo: {"files": [], "dirs": {}}}

    for token in _get_git_tree(author, repo, sha):
        path_parts = token["path"].split("/")
        current = tree[repo]
        for part in path_parts[:-1]:
            current = current["dirs"].setdefault(part, {"files": [], "dirs": {}})
        if token["type"] == "tree":
            current["dirs"].setdefault(path_parts[-1], {"files": [], "dirs": {}})
        elif token["type"] == "blob":
            current["files"].append(path_parts[-1])
    return tree


def parse_github_url(url):
    """Parse the GitHub URL to extract author and repo."""
    parsed_url = urlparse(url)
    path_parts = parsed_url.path.strip("/").split("/")
    if len(path_parts) >= 2:
        return f"{path_parts[0]}/{path_parts[1]}"
    else:
        raise GitError("Invalid GitHub URL format")


def print_tree(tree, prefix=""):
    """Print the tree structure."""
    for key in sorted(tree.keys()):
        if isinstance(tree[key], dict):
            print(f"{prefix}├── {key}/")
            print_tree(tree[key]["dirs"], prefix + "│   ")
            for file in tree[key]["files"]:
                print(f"{prefix}│   ├── {file}")
        else:
            print(f"{prefix}├── {key}")


def main():
    """Main function to interact with the user and generate the repo tree."""
    while True:
        try:
            repo_url = input("Enter the GitHub repository URL or author/repo: ").strip()
            if not repo_url:
                print("Repository URL cannot be empty.")
                continue
            if "github.com" in repo_url:
                repo_url = parse_github_url(repo_url)
            tree = git_tree(repo_url)
            print_tree(tree)
            break
        except GitError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
