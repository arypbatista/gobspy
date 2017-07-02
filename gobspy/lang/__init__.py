import sys


from .preprocessor import preprocess
from .runner import run_program


class Gobspy:

    def run(self, text, filepath=None, initial_board=None):
        code = preprocess(text)
        result = run_program(code)
        return result

Gobstones = Gobspy

run = lambda *args, **kwargs: Gobspy().run(*args, **kwargs)
