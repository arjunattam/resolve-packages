import sys
import npm
import nuget
import github


if __name__ == '__main__':
    has_package_name = len(sys.argv) > 2
    registry = sys.argv[1]

    if registry == 'nuget':
        if has_package_name:
            names = [sys.argv[2]]
        else:
            names = nuget.get_most_downloaded_nuget_packages()

        for name in names:
            version = nuget.get_version(name)
            url = nuget.get_repo_url(name)

            if version and url:
                github.resolve_to_commit(name, url, version)
            else:
                print(f'{name}: could not resolve to url or version')

    elif registry == 'npm':
        if has_package_name:
            package_name, version = sys.argv[2], sys.argv[3]
            packages = [{'name': package_name, 'version': version}]
        else:
            packages = npm.get_most_depended_upon_npm_packages(1)

        for package in packages:
            url = npm.get_repo_url(package['name'])

            if url:
                github.resolve_to_commit(**package, url=url)
            else:
                print(f'{name}: repository url not resolved')
