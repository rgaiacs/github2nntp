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

import io
import os
import logging
import nntplib

NNTPSERVER = os.environ['NNTPSERVER']

def post(n, m):
    """
    Post a message to a newsgroup.

    :param n: newsgroup name
    :type n: str
    :param m: message
    :type m: str
    """
    s = nntplib.NNTP(NNTPSERVER)
    try:
        can_post = s.group(n)
    except nntplib.NNTPError as err:
        logging.error('Can\'t select news group.\n\t{0}'.format(err))
        can_post = False
    if can_post != False:
        try:
            s.post(io.BytesIO(m.encode()))
            logging.info('Message posted.')
        except nntplib.NNTPError as err:
            logging.error('Message not posted.\n\t{0}'.format(err))
    s.quit()
