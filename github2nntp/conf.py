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

"""
Parse Configuration and Status file
"""

"""
Configuration file
------------------

It store the GitHub token to be used and the list of repositories to fetch the
newsgroup to feed.

The line has the following structure::

    newsgroup.name	owner	repo

Note that the fields are separate by tabs.
"""

def conf_parse_line(l):
    """
    Parse one line of the configuration file.

    :param l: line
    :type l: str
    """
    ll = l.split('\t')
    return {'newsgroup': ll[0],
            'owner': ll[1],
            'repo': ll[2]}

"""
Status file
-----------

It store informations of the list of repositories used in the previous time.

The file has the following strucuture::

    newsgroup.name owner repo time
"""

def status_parse_line(l):
    """
    Parse one line of the status file.

    :param l: line
    :type l: str
    """
    ll = l.split('\t')
    return {'newsgroup': ll[0],
            'owner': ll[1],
            'repo': ll[2],
            'time': ll[3]}
