from .board import Board
from traceback import format_stack, extract_stack, format_list

class State:

    def __init__(self):
        self.board = Board().randomize()

    def backtrace(self, message=''):
        return message + '\n' + ''.join(format_list(extract_stack()[:-2]))

state = State()
