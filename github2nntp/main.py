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

import os
import time
import datetime
import logging
import github2nntp.conf as conf
import github2nntp.issues as issues
import github2nntp.comments as comments

"""
GitHub API have a rate limit. For requests using Basic Authentication, OAuth, or
client ID and secret, you can make up to 20 requests per minute. For
unauthenticated requests, the rate limit allows you to make up to 5 requests per
minute.

From: http://developer.github.com/v3/search/#rate-limit
"""
NUMBER_REQUEST =  0  # The number of request in the last minute.
AU_MAX_REQUEST = 20  # The max number of request per minute when authenticated
OT_MAX_REQUEST =  5  # The max number of request per minute when unauthenticated
TIME_LAST_REQUEST = time.time()

def check_time(token_enable=False):
    """
    This function check the number of request per minute and wait some time if
    need.
    """
    now = time.time()
    if(now - TIME_LAST_REQUEST > 60):
        pass
    else:
        if(token_enable and NUMBER_REQUEST < AU_MAX_REQUEST):
            pass
        elif(not token_enable and NUMBER_REQUEST < OT_MAX_REQUEST):
            pass
        else:
            logging.info('Go to sleep for {} seconds.'.format(now -
                TIME_LAST_REQUEST))
            time.sleep(int(now - TIME_LAST_REQUEST) + 1)

def write2status(f, news, owner, repo):
    """
    Write the status information.

    :param f: the file
    :type f: _io.TextIOWrapper
    :param news: the newsgroup name
    :typee news: str
    :param owner: the owner of the repo
    :type owner: str
    :param repo: the name of the repo
    :type repo: str
    """
    f.write('{}\t{}\t{}\t{:%Y-%m-%dT%H:%M:%S}Z'.format(news,
            owner, repo, datetime.datetime.utcnow()))

def run(fconf='~/.github2nntp.conf', fstatus='~/.github2nntp.status',
        ftoken='~/.github2nntp.token'):

    news = []
    olds = []
    status = []

    # Try load token file
    try:
        with open(os.path.expanduser(ftoken), 'r') as f:
            token = f.readline().rstrip('\n')
    except FileNotFoundError as err:
        logging.info('{} not found. Ignoring.'.format(ftoken))
        token = None

    # Try load the status file
    try:
        with open(os.path.expanduser(fstatus), 'r') as f:
            for l in f.readlines():
                status.append(conf.status_parse_line(l))
    except FileNotFoundError as err:
        logging.info('{} not found. Ignoring.'.format(fstatus))


    # Load the config file
    with open(os.path.expanduser(fconf), 'r') as f:
        for l in f.readlines():
            tmp = conf.conf_parse_line(l)
            for s in status:
                if (tmp['newsgroup'] == s['newsgroup'] and
                        tmp['owner'] == s['owner'] and
                        tmp['repo'] == s['repo']):
                    olds.append(s)
                    break
            else:
                news.append(tmp)

    # Write information new information in the status files
    with open(os.path.expanduser(fstatus), 'w') as f:
        # Old repos
        for l in olds:
            check_time()
            issues.send2nntp(token,
                    l['newsgroup'],
                    l['owner'],
                    l['repo'],
                    l['time'])
            NUMBER_REQUEST += 1

            check_time()
            comments.send2nntp(token,
                    l['newsgroup'],
                    l['owner'],
                    l['repo'],
                    l['time'])
            NUMBER_REQUEST += 1

            write2status(l['newsgroup'], l['owner'], l['repo'])

        # New repos
        for l in news:
            check_time()
            issues.send2nntp(token,
                    l['newsgroup'],
                    l['owner'],
                    l['repo'],
                    None)
            NUMBER_REQUEST += 1

            check_time()
            comments.send2nntp(token,
                    l['newsgroup'],
                    l['owner'],
                    l['repo'],
                    None)
            NUMBER_REQUEST += 1

            write2status(l['newsgroup'], l['owner'], l['repo'])

def main():
    """GitHub2NNTP"""
    import argparse

    parser = argparse.ArgumentParser(description='Gateway from GitHub to NNTP.')
    parser.add_argument('-c', '--conf', type=str,
            default=os.path.expanduser('~/.github2nntp.conf'),
            help='configuration file')
    parser.add_argument('-s', '--status', type=str,
            default=os.path.expanduser('~/.github2nntp.status'),
            help='status file')
    parser.add_argument('-l', '--log', type=str,
            default=os.path.expanduser('~/.github2nntp.log'),
            help='log file')
    parser.add_argument('-t', '--token', type=str,
            default=os.path.expanduser('~/.github2nntp.token'),
            help='token file')

    args = parser.parse_args()

    logging.basicConfig(filename=args.log, filemode='w',  level=logging.INFO)

    logging.info('Started')
    run(args.conf, args.status, args.token)
    logging.info('Finished')
