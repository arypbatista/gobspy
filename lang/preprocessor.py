import re

IMPORTS = [
    'from lang.builtins import *'
]

class Preprocessor:

    def process(self, text):
        res = text
        res = self.process_procedures(res)
        res = self.process_functions(res)
        res = self.process_main(res)
        return res

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
