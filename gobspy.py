import lang
from lang.utils import read_file


FILE = './example.gpy'

lang.run(read_file(FILE), FILE)

print(lang.state.board)
