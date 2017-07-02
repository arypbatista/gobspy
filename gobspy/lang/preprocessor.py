from .exceptions import StaticException

import re

IMPORTS = [
    'from lang.builtins import *'
]

colon_keyword = re.compile('(if|else|def|while)')

class PreprocessorException(StaticException):
    pass

class Preprocessor:

    def process(self, text):
        res = text
        self.check_root_commands(text)
        res = self.process_procedures(res)
        res = self.process_functions(res)
        res = self.process_main(res)
        res = self.process_command_separator(res)
        res = self.remove_brackets(res)
        res = self.fix_colons(res)
        return res

    def fix_colons(self, text):
        out = ''
        for l in text.split('\n'):
            if colon_keyword.match(l) is not None:
                if l.strip()[-1] != ':':
                    out += l + ':'
                else:
                    out += l
            else:
                out += l
            out += '\n'
        return out

    def remove_brackets(self, text):
        return text.replace('{', '').replace('}', '')

    def process_command_separator(self, text):
        indentation = re.compile('^\s*')
        semicollon = re.compile(';\s*')
        out = []
        for l in text.split('\n'):
            if ';' in l:
                match = indentation.match(l)
                ind = ''
                if match is not None:
                    ind = match.group()
                out.append(('\n' + ind).join(semicollon.split(l)))
            else:
                out.append(l)
        return '\n'.join(out)

    def check_root_commands(self, text):
        root_commands = list(re.finditer(r'^[^\#dfp\s][^eur\s][^fno\s]', text, re.MULTILINE))
        if len(root_commands) > 0:
            raise PreprocessorException('You cannot call commands outside a procedure or a function definition')

    def process_procedures(self, text):
        text = text.replace('procedure ', 'proc ')
        return text.replace('proc ', 'def ')

    def process_main(self, text):
        return text + '\n'.join([
            '', '',
            '# Call Main procedure',
            'Main()'
        ])

    def process_functions(self, text):
        res = text + '\n\n# Define functions'
        res = res.replace(r"function\s+([a-zA-Z]+)", 'func')
        for match in re.finditer(r"func\s+([a-zA-Z]+)", text):
            name = match.group(1)
            res += '\n%s = define_function(%s)' % (name, name)
        res = res.replace('func ', 'def ')
        return res



preprocess = Preprocessor().process
