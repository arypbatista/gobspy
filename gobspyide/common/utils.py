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

import os
import sys
import re
import colorsys
import webbrowser
import tempfile
import atexit
import shutil

try:
  import hashlib as md5
except ImportError:
  import md5

#### Various utility functions

VERSION = 0, 1, 0

def version_number():
  return '%s.%s.%s' % VERSION

class SourceException(Exception):
  def __init__(self, msg, area):
    self.msg = msg
    self.area = area
  def __repr__(self):
    s = ''
    if self.area:
      s += '\n%s\n' % (self.area,)
    s += '%s\n' % (indent(self.msg),)
    return s
  def error_type(self):
    return 'Error'

class StaticException(SourceException):
  pass

class DynamicException(SourceException):
  pass

def trim(x):
  return x.strip(' \t\r\n')

_blanks = re.compile('[ \t\r\n]+')
def trim_blanks(x):
  return trim(_blanks.sub(' ', x))

def nonempty(x):
  return x != ''

def read_file(fn):
  f = file(fn, 'r')
  c = f.read()
  f.close()
  return c

## set

def set_new(xs=[]):
  d = {}
  for x in xs: d[x] = 1
  return d

def set_add(s, x):
  s[x] = 1

def set_add_change(s, x):
  if x not in s:
    s[x] = 1
    return True
  return False

def set_extend(s1, s2):
  for k, v in s2.items():
    s1[k] = v

def set_remove(s1, s2):
  for k, v in s2.items():
    if k in s1:
      del s1[k]

## tokset
## Set with an associated token.
## When joining two sets, it always keeps
## the token that occurs first in the input.

Tokset_key = lambda tree: tree.pos_begin.start

tokset_new = set_new

def tokset_new_from_dict(d):
  return d

def tokset_empty(s):
  return len(s) == 0

def tokset_extend_change(s1, s2):
  change = False
  for k, v in s2.items():
    if k not in s1:
      s1[k] = v
      change = True
    elif Tokset_key(v) < Tokset_key(s1[k]):
      s1[k] = v
  return change

tokset_extend = tokset_extend_change

def tokset_union(s1, s2):
  res = {}
  for k, v in s1.items():
    res[k] = v
  tokset_extend_change(res, s2)
  return res

def tokset_difference(s1, s2):
  res = {}
  for k, v in s1.items():
    if k not in s2:
      res[k] = v
  return res

def seq_sorted(xs, key=lambda x: x):
  xs = map(lambda x: (key(x), x), xs)
  xs.sort(lambda a, b: cmp(a[0], b[0]))
  return map(lambda xy: xy[1], xs)

def seq_reversed(xs):
  ys = []
  for x in xs:
    ys.insert(0, x)
  return ys

def seq_no_repeats(xs):
  res = []
  for x in xs:
    if x not in res:
      res.append(x)
  return res

def seq_insert(xs, idx, ys):
  assert idx >= 0
  for y in ys:
    xs.insert(idx, y)
    idx += 1

def is_int(x):
  if not x:
    return False
  if not isinstance(x, str):
    return False
  if len(x) == 0:
    return False
  for c in x:
    if c not in '0123456789':
      return False
  return True

##

def dict_min_value(xs, key=lambda x: x):
  for x in seq_sorted(xs.values(), key):
    return x

def indent(msg, n=4):
  return '\n'.join(map(lambda m: n * ' ' + m, msg.split('\n')))

def expand_tabs(x):
  return x.replace('\t', ' ')

def std_warn(x):
  sys.stderr.write(repr(x))

def show_string(s):
  s = s[1:-1]
  r = ''
  conv = {
    'a': '\a',
    'b': '\b',
    'f': '\f',
    'n': '\n',
    'r': '\r',
    't': '\t',
    'v': '\v',
    '\\': '\\',
    '\"': '\"'
  }
  i = 0
  while i < len(s):
    if s[i] == '\\' and i + 1 < len(s):
      c = s[i + 1]
      r += conv.get(c, c)
      i += 2
    else:
      r += s[i]
      i += 1
  return r

##

def md5sum(s):
  return md5.md5(s).hexdigest()

##

def hsv(h, s, v):
  r, g, b = colorsys.hsv_to_rgb(h, s, v)
  return '#%.2x%.2x%.2x' % (int(r * 255), int(g * 255), int(b * 255))

## Parser for option switches

def default_options(option_switches):
  opt = {}
  for o in option_switches:
    o = o.split(' ')
    sw = o[0][2:]
    if sw[:3] == 'no-':
      neg = True
      sw = sw[3:]
    else:
      neg = False
    if len(o) == 1:
      opt[sw] = neg
    else:
      opt[sw] = []
  return opt

def parse_options(option_switches, args, max_args=None):
  arguments = []
  opt = default_options(option_switches)
  i = 1
  n = len(args)
  while i < len(args):
    o = None
    for oi in option_switches:
      oi = oi.split(' ')
      if oi[0] == args[i]:
        o = oi
        break
    if o == None:
      if len(arguments) == max_args:
        return False
      arguments.append(args[i])
      i += 1
      continue

    sw = o[0][2:]
    if len(o) == 1:
      if sw[:3] == 'no-':
        neg = True
        sw = sw[3:]
      else:
        neg = False
      opt[sw] = not neg
      i += 1
    else:
      k = 1
      i += 1
      while k < len(o):
        if i >= n: return False
        opt[sw].append(args[i])
        i += 1
        k += 1
  return arguments, opt

##

Temp_html_dir = None

def temp_html_dir():
  global Temp_html_dir
  if Temp_html_dir == None:
    Temp_html_dir = tempfile.mkdtemp()
    atexit.register(_temp_html_dir_cleanup)
  return Temp_html_dir

def _temp_html_dir_cleanup():
  if Temp_html_dir != None:
    shutil.rmtree(Temp_html_dir)

def open_html(fn):
  webbrowser.open(fn, autoraise=True)

def open_temp_html(prefix, contents):
  fn = os.path.join(temp_html_dir(), prefix + '.html')
  f = file(fn, 'w')
  f.write(contents)
  f.close()
  open_html(fn)

##

def read_stripped_lines(f):
  def next_line():
    while True:
      l = f.readline()
      if l == '' or l.strip(' \t\r\n') == '%%': return False
      l = l.strip(' \t\r\n').split('#')[0].strip(' \t\r\n')
      if l != '': return re.sub('[ \t]+', ' ', l)
  lines = []
  while True:
    l = next_line()
    if not l: break
    lines.append(l)
  return lines
