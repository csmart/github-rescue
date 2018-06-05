#!/usr/bin/env

# This is a simple script which will mirror all of your repositories from
# github. This makes is really easy to then push those repoistories to a new
# git service, such as gitlab.
#
# Note that I do not currently support private repositories, but that would
# be relatively easy to add.

from __future__ import print_function

import argparse
import datetime
import json
import os
import subprocess
import sys
import random

from github import Github as github


def get_github_projects(github_token, username):
    g = github(github_token)
    for repo in g.get_user(login=username).get_repos():
        yield('https://github.com', repo.full_name)


def _ensure_path(path):
    if not path:
        return

    full = []
    for elem in path.split('/'):
        full.append(elem)
        if not os.path.exists('/'.join(full)):
            os.makedirs('/'.join(full))


def sync(github_token, username):
    starting_dir = os.getcwd()
    projects = []
    for res in list(get_github_projects(github_token, username)):
        if len(res) == 3:
            projects.append(res)
        else:
            projects.append((res[0], res[1], res[1]))

    random.shuffle(projects)

    for base_url, project, subdir in projects:
        print('%s Considering %s %s'
              %(datetime.datetime.now(), base_url, project))
        os.chdir(starting_dir)

        if os.path.isdir(subdir):
            os.chdir(subdir)

            print('%s Updating %s'
                  %(datetime.datetime.now(), project))
            try:
                subprocess.check_call(
                    ['git', 'remote', 'update'])
            except Exception as e:
                print('%s FAILED: %s'
                      %(datetime.datetime.now(), e))
        else:
            git_url = os.path.join(base_url, project)
            _ensure_path('/'.join(subdir.split('/')[:-1]))

            print('%s Cloning %s'
                  %(datetime.datetime.now(), project))
            subprocess.check_call(
                ['ionice', '-c', 'idle', 'git', 'clone',
                 '--mirror', git_url, subdir])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--github_token', help='Your github access token')
    parser.add_argument('--username', help='The github username to mirror')
    args = parser.parse_args()

    broken = False
    if not args.github_token:
        print('You must specify a github API access token using '
              '--github_token!')
        broken = True
    if not args.username:
        print('You must specify a github username to mirror using --username!')
        broken = True
    if broken:
        sys.exit(1)

    sync(args.github_token, args.username)


if __name__ == '__main__':
    main()
    
