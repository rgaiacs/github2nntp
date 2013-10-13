# GitHub2NNTP
# Copyright (C) 2013  Raniere Silva
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import logging

def retrieve(t, o, r, s):
    """
    Retrieve comments from repository.

    :param t: token
    :type t: str
    :param o: owner
    :type o: str
    :param r: repo
    :type r: str
    :param s: since
    :type s: str
    :return: the JSON return from the server
    :rtype: str
    """
    import urllib.request
    import urllib.error

    # Authentication
    passman = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    passman.add_password(None, 'https://api.github.com', t, 'x-oauth-basic')
    authhandler = urllib.request.HTTPBasicAuthHandler(passman)
    opener = urllib.request.build_opener(authhandler)
    urllib.request.install_opener(opener)

    # Set url
    if s:
        url = 'https://api.github.com/repos/{}/{}/issues/comments?since={}'.format(o,
                r, s)
    else:
        url = 'https://api.github.com/repos/{}/{}/issues/comments'.format(o,
                r)
    logging.info('Downloading {}'.format(url))

    # Request
    try:
        response = urllib.request.urlopen(url)
    except urllib.error.HTTPError as err:
        logging.critical(err)
        sys.exit()
    return response.read().decode()

def conv(t):
    """
    Convert JSON
    """
    import json

    return json.loads(t)

def write_new(n, t, d):
    """
    Process dict to news.
    """
    import email.utils

    return 'Date: {}\nFrom: {}\nMessage-ID: {}\nNewsgroups: {}\n' \
            'Path: github2nntp.local\nSubject: {}\n\n{}\nLink: {}\n'.format(
            d['updated_at'],
            d['user']['login'],
            email.utils.make_msgid(),
            n,
            t,
            d['body'],
            d['html_url'])

def send2nntp(g, o, r, n, t, s):
    """
    Send issues to nntp server.

    :param g: newsgroup
    :type g: str
    :param o: owner
    :type o: str
    :param r: repo
    :type r: str
    :param s: since
    :type s: str
    """
    import github2nntp.nntp as nntp

    a = retrieve(o, r, n, s)
    for i in conv(a):
        logging.info('Processing comment {} of issue {}'.format(i['id'], n))
        nntp.post(g, write_new(g, t, i))

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='GitHub2NNTP comments from issues retrieve.')
    parser.add_argument('-o', '--owner', type=str, required=True,
            help='owner of the repository')
    parser.add_argument('-r', '--repo', type=str, required=True,
            help='name of the repository')
    parser.add_argument('-n', '--number', type=str, required=True,
            help='number of the issue')
    parser.add_argument('-s', '--since', type=str,
            help='only issues updated after YYYY-MM-DDTHH:MM:SSZ')

    args = parser.parse_args()

    print(retrieve(args.owner, args.repo, args.number, args.since))
