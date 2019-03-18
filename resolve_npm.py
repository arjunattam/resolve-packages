# Resolves npm package version to commit id using github tags
#
# To run on request package (version 2.88.0)
# python resolve_npm.py request 2.88.0

import os
import re
import sys
import bs4
import requests


def get_package_info(package_name):
    """Gets package.json info for package_name on npm"""
    r = requests.get(f'https://api.npms.io/v2/search?q={package_name}&size=1')
    response_json = r.json()
    
    if 'results' in response_json:
        result = response_json['results'][0]
        return result['package']


def get_repo_url(package_name):
    """Finds repo url from package.json on npm"""
    package_info = get_package_info(package_name)

    if package_info:
        return package_info['links']['repository']


def _github_headers():
    token = os.environ.get('GITHUB_TOKEN')

    if token:
        return {'Authorization': f'token {token}'}


def get_github_tag(repo_url, version):
    """Finds github release for a version on repo_url
       https://developer.github.com/v3/repos/#list-tags"""
    pattern = re.compile('github\.com/(.+)/(.+)')
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
    return tag['commit']['sha'] if tag else None


def _parse_section(section):
    name = section.find('h3').contents[0]
    latest_version = section.find('span').contents[2]
    return {'name': name, 'version': latest_version}


def get_most_depended_upon_npm_packages():
    """Fetches package and version from npmjs.com. Since there is no
    API to fetch this, we scrape it off the page (not ideal, yes)."""
    r = requests.get('https://www.npmjs.com/browse/depended')
    soup = bs4.BeautifulSoup(r.content, 'html.parser')
    sections = soup.find_all('section')
    return list(map(_parse_section, sections))


def resolve_package_to_commit(name, version):
    url = get_repo_url(name)

    if url:
        commit = get_resolved_commit(url, version)

        if commit:
            print(f'{name}: {version} resolved to {commit}')
        else:
            print(f'{name}: found repo, cannot resolve to commit')
    else:
        print(f'{name}: repository url not resolved')


if __name__ == '__main__':
    has_specified_package = len(sys.argv) > 1

    if has_specified_package:
        package_name, version = sys.argv[1], sys.argv[2]
        packages = [{'name': package_name, 'version': version}]
    else:
        packages = get_most_depended_upon_npm_packages()
    
    for package in packages:
        resolve_package_to_commit(**package)
