"""
import lang.i18n as i18n
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Execute Gobspy.')
    parser.add_argument('-l', '--language', default='es',
        help='language used for code translation')

    args = parser.parse_args()
    return args

args = parse_args()

i18n.set_language(args.language)
"""
