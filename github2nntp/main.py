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
import datetime
import logging
import github2nntp.conf as conf
import github2nntp.issues as issues

def run(fconf='~/.github2nntp.conf', fstatus='~/.github2nntp.status'):
    news = []
    olds = []
    status = []
    try:
        with open(os.path.expanduser(fstatus), 'r') as f:
            for l in f.readlines():
                status.append(conf.status_parse_line(l))
    except FileNotFoundError as err:
        logging.info('{} not found. Ignoring.'.format(fstatus))
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
    with open(os.path.expanduser(fstatus), 'w') as f:
        for l in olds:
            issues.send2nntp(l['newsgroup'],
                    l['owner'],
                    l['repo'],
                    l['time'])
            f.write('{} {} {} {:%Y-%m-%dT%H:%M:%S}Z'.format(l['newsgroup'],
                    l['owner'],
                    l['repo'],
                    datetime.datetime.utcnow()))
        for l in news:
            issues.send2nntp(l['newsgroup'],
                    l['owner'],
                    l['repo'],
                    None)
            f.write('{} {} {} {:%Y-%m-%dT%H:%M:%S}Z'.format(l['newsgroup'],
                    l['owner'],
                    l['repo'],
                    datetime.datetime.utcnow()))

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

    args = parser.parse_args()

    logging.basicConfig(filename=args.log, filemode='w',  level=logging.INFO)

    logging.info('Started')
    run(args.conf, args.status)
    logging.info('Finished')
