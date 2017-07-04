import sys

from .builtins import builtins
from .board import Board
from .utils import StringIO
from .state import state
from .i18n import translate as t
from .exceptions import to_message, GobspyException, PythonException

class GobspyResult:

    def __init__(self, pycode, out, final_board, error=''):
        self.final_board = final_board
        self.out = out
        self.result = []
        self.pycode = pycode
        self.error = error

    def failed(self):
        return self.final_board is None

class GobspyRunner:

    def run(self, code, filepath=t('main program'), initial_board=None):
        state.init()
        if initial_board:
            state.board = initial_board

        old_output = sys.stdout
        redirected_output = sys.stdout = StringIO()
        final_board = None
        error_message = ''

        try:
            exec(code, builtins, builtins)
            final_board = state.board
            sys.stdout = old_output
        except Exception as e:
            sys.stdout = old_output
            if not isinstance(e, GobspyException):
                exception = PythonException(e)
            else:
                exception = e
            error_message = to_message(filepath, exception)

        return GobspyResult(code, redirected_output.getvalue(), final_board, error_message)


def run_program(code, filepath=t('main program'), initial_board=None):
    return GobspyRunner().run(code, filepath, initial_board)
