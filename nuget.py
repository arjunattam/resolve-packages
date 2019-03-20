import re
import bs4
import requests
from github import resolve_to_commit


def _package_name(table_row):
    name_td = table_row.contents[3]
    name_link = name_td.contents[0]
    return name_link.contents[0]


def get_most_downloaded_nuget_packages():
    """Scraping off the web page due to lack of an API.

    This page has two tables: first table has all packages (including ones from MS),
    second table has only community packages. We look at community packages."""
    r = requests.get('https://www.nuget.org/stats/packages')
    soup = bs4.BeautifulSoup(r.content, 'html.parser')
    packages_tbody = soup.find_all('tbody')[1] # change to 0 for all packages
    names = list(map(_package_name, packages_tbody.find_all('tr')))
    return names


def get_version(name):
    """Earlier version of this method used the versions API, but that was not working
    properly for packages that have many releases.
    
    API: https://api.nuget.org/v3-flatcontainer/{name}/index.json"""
    r = requests.get(f'https://www.nuget.org/packages/{name}/')
    soup = bs4.BeautifulSoup(r.content, 'html.parser')
    version_tr = soup.find('tr', {'class': 'bg-info'})
    version_td = version_tr.contents[3]
    version_link = version_td.contents[1]
    return version_link.contents[0].strip()


def _is_github_url(url):
    pattern = re.compile('github\.com/(.+)/(.+)')
    return re.search(pattern, url)


def _clean_url(url):
    """Removes .git from the url"""
    pattern = re.compile('^https?://github.com/(.+)/(.+)')
    match = re.search(pattern, url)
    owner, repo = match.groups()

    if repo.endswith('.git'):
        repo = repo.replace('.git', '')

    return f'https://github.com/{owner}/{repo}'


def get_repo_url(name):
    """This prototype scrape this info from the web page. We could potentially use the API
       for package metadata, but that has some issues:

    API docs: https://docs.microsoft.com/en-us/nuget/api/registration-base-url-resource

    1. List API result (all versions) does not expose the repository url, which is available
       on the webpage. We could potentially extract repo url from the license url or project homepage,
       but it seems worth it to utilise the existing effort that has been made to get the repo url
       on the webpage.
    2. API response for specific version does not return any urls in the response.
    """
    r = requests.get(f'https://www.nuget.org/packages/{name}/')
    soup = bs4.BeautifulSoup(r.content, 'html.parser')
    repo_link_els = soup.find_all('a', {'data-track': 'outbound-repository-url'})

    if repo_link_els:
        repo_link_el = repo_link_els[0]
        return _clean_url(repo_link_el['href'])

    project_url_els = soup.find_all('a', {'data-track': 'outbound-project-url'})

    if project_url_els:
        project_url_el = project_url_els[0]
        href = project_url_el['href']
        return _clean_url(href) if _is_github_url(href) else None
