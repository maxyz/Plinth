#
# This file is part of Plinth.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""
Plinth module to configure a Deluge web client.
"""

from gettext import gettext as _

from plinth import cfg


depends = ['plinth.modules.apps']


def init():
    """Initialize the Deluge module."""
    menu = cfg.main_menu.get('apps:index')
    menu.add_urlname(_('BitTorrent (Deluge)'), 'glyphicon-magnet',
                     'deluge:index', 60)
