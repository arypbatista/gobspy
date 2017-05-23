import re

IMPORTS = [
    'from lang.builtins import *'
]

class PreprocessorException(Exception):
    pass

class Preprocessor:

    def process(self, text):
        res = text
        self.check_root_commands(text)
        res = self.process_procedures(res)
        res = self.process_functions(res)
        res = self.process_main(res)
        return res

    def check_root_commands(self, text):
        root_commands = list(re.finditer(r'^[^\#dfp\s][^eur\s][^fno\s]', text, re.MULTILINE))
        if len(root_commands) > 0:
            raise PreprocessorException('You cannot call commands outside a procedure or a function definition')

    def process_procedures(self, text):
        return text.replace('proc ', 'def ')

    def process_main(self, text):
        return text + '\n'.join([
            '', '',
            '# Call Main procedure',
            'Main()'
        ])

    def process_functions(self, text):
        res = text + '\n\n# Define functions'
        for match in re.finditer(r"func\s+([a-zA-Z]+)", text):
            name = match.group(1)
            res += '\n%s = define_function(%s)' % (name, name)
        res = res.replace('func ', 'def ')
        return res



preprocess = Preprocessor().process
