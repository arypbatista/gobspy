import lang
from lang.utils import read_file
from lang.builtins import *
from traceback import format_exc


FILE = './example.gpy'

code = lang.preprocess(read_file(FILE))




print(code)
print('##############')
try :
    exec(code, globals(), locals())
except Exception as e:
    print format_exc(e).replace('<string>', FILE)
print('##############')
print(lang.state.board)
