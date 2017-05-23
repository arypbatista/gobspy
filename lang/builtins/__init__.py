from .builtins import builtins
from ..i18n import translate as t

for k in builtins.keys():
    if k[0] != '_':
        try:
            value = builtins[k]
            code = '%s = value' % k
            code = '%s = value' % t(k)
            exec(code)
        except e:
            pass
