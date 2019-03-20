import os
import re
import requests


def resolve_to_commit(name, url, version):
    commit = get_resolved_commit(url, version)

    if commit:
        print(f'{name}: {version} resolved to {commit}')
    else:
        print(f'{name}: found repo, cannot resolve {version} to commit')


def _github_headers():
    token = os.environ.get('GITHUB_TOKEN')
    return {'Authorization': f'token {token}'} if token else None


def get_github_tag(repo_url, version):
    """Finds github release for a version on repo_url.
    API docs: https://developer.github.com/v3/repos/#list-tags"""
    pattern = re.compile('^https?://github.com/(.+)/([^/]+)')
    match = re.search(pattern, repo_url)
    owner, repo = match.groups()
    r = requests.get(f'https://api.github.com/repos/{owner}/{repo}/tags', headers=_github_headers())

    if r.status_code == 200:
        repo_tags = r.json()
        filtered = list(filter(lambda x: x['name'] == version or x['name'] == f'v{version}',
                               repo_tags))
        return filtered[0] if filtered else None
    else:
        print(f'github api error: {r.status_code}')


def get_resolved_commit(repo_url, version):
    tag = get_github_tag(repo_url, version)
    return tag['commit']['sha'][0:8] if tag else None
