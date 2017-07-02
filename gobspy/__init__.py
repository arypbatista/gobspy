import lang
from lang.utils import read_file
import lang.i18n as i18n
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Execute Gobspy.')
    parser.add_argument('file')
    parser.add_argument('-l', '--locale', default='es',
        help='locale used for code translation')
    parser.add_argument('--print-compiled', action='store_const', const=True,
        help='print compiled program')

    args = parser.parse_args()
    return args



def main():
    args = parse_args()
    i18n.set_language(args.locale)
    result = lang.run(read_file(args.file), args.file)

    if result.error is None:
        print(lang.state.board)
    else:
        print(result.error)
    if args.print_compiled:
        print(result.pycode)

if __name__ == '__main__':
    main()
