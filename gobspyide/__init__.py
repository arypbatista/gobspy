#!/usr/bin/python
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

import sys
import encodings.utf_8

from .gui import app
from .common import tools

import multiprocessing


def main():
    multiprocessing.freeze_support()
    gui_class = gui.app.GUI
    g = gui_class()
    g.geometry("640x480")
    if len(sys.argv) == 2:
        fn = sys.argv[1]
        if tools.formats.is_board_filename(fn):
            g.board_load_fn(fn)
        else:
            g.file_open_fn(fn)
    g.mainloop()


if __name__ == '__main__':
    main()
