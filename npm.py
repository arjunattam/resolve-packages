import re
import sys
import bs4
import requests
from github import resolve_to_commit


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

    if package_info and package_info.get('links'):
        links = package_info['links']

        if links.get('repository'):
            return links['repository']


def _parse_section(section):
    name = section.find('h3').contents[0]
    latest_version = section.find('span').contents[2]
    return {'name': name, 'version': latest_version}


def get_most_depended_upon_npm_packages(page):
    """Fetches package and version from npmjs.com. Since there is no
    API to fetch this, we scrape it off the page (not ideal, yes)."""
    offset = (page - 1) * 36 # page length is 36
    r = requests.get(f'https://www.npmjs.com/browse/depended?offset={offset}')
    soup = bs4.BeautifulSoup(r.content, 'html.parser')
    sections = soup.find_all('section')
    return list(map(_parse_section, sections))
