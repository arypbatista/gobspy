import sys
from cStringIO import StringIO
from .builtins import builtins
from .state import state
from .preprocessor import preprocess
from .board import Board
from traceback import format_exc

class GobspyResult:

    def __init__(self, pycode, out, final_board):
        self.final_board = final_board
        self.out = out
        self.result = []
        self.pycode = pycode

class Gobspy:

    def run(self, text, filepath=None, initial_board=None):
        state.init()
        if initial_board:
            state.board = initial_board
        code = preprocess(text)
        old_output = sys.stdout
        redirected_output = sys.stdout = StringIO()
        try:
            exec(code, builtins, builtins)
        except Exception as e:
            print(format_exc().replace('<string>', filepath))
        sys.stdout = old_output
        return GobspyResult(code, redirected_output.getvalue(), state.board)

Gobstones = Gobspy

run = lambda *args, **kwargs: Gobspy().run(*args, **kwargs)
