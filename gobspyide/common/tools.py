# -*- coding: utf-8 -*-
#
# Copyright (C) 2011-2017 Ary Pablo Batista <arypbatista@gmail.com>, Pablo Barenbaum <foones@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

import re
from gobspy import lang
from gobspy.lang.builtins import builtins as gbuiltins
from gobspy.lang.board import formats
from . import i18n, utils
import tokenize

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

def fake_bof(self):
  pass


BoardViewerGeometry = "480x480"
DefaultBoardSize = 'random'
run = lang.run
tokenize = tokenize.tokenize
Board = lang.board.Board

class GobspyBuiltins:
    def __init__(self):
        self.nothing = None
        self.COLORS_BY_INITIAL = dict([ (c.i18n_initial(), c) for c in gbuiltins['COLORS']]),
        directions = gbuiltins['DIRECTIONS_BY_NAME']
        self.NORTH = directions['North']
        self.WEST  = directions['West']
        self.EAST  = directions['East']
        self.SOUTH = directions['South']

builtins = GobspyBuiltins()

formats  = formats
