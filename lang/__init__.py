from .builtins import builtins
from .state import state
from .preprocessor import preprocess
from traceback import format_exc

def run(text, filepath=None):
    code = preprocess(text)
    try:
        exec(code, builtins, builtins)
    except Exception as e:
        print format_exc(e).replace('<string>', filepath)
