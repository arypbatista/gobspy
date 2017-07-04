from .utils import indent, parse
from .i18n import translate as t
from traceback import format_exc

class BoardFormatException(Exception):
    pass

class GobspyException(Exception):

    def __init__(self, message, area=None):
        if isinstance(message, list):
            mi = t(message[0])
            m = message[0]
            for i in range(len(message[1])):
                mi = mi % t(str(message[1][i]))
                m = m % message[1][i]
            self.message = m
            self.i18n_message = mi
            self.raw_message = message
        else:
            self.message = message
            self.i18n_message = message
            self.raw_message = [message, (None,)]
        self.area = area

    def __repr__(self):
        s = ''
        if self.area:
            s += '\n%s\n' % (self.area,)
        s += '%s\n' % (indent(self.message),)
        return s

    def error_type(self):
        return t('Error')

    def error_class(self):
        return type(self).__name__

class PythonException(GobspyException):

    def __init__(self, e):
        message = ''
        for i in range(len(e.args)):
            message += str(e.args[i]) + ' '
        message = message.strip()
        super(PythonException, self).__init__(message, format_exc(e))
        self.exception = e

    def error_class(self):
        return type(self.exception).__name__


class SourceException(GobspyException):
    pass


class StaticException(SourceException):
    pass


class DynamicException(SourceException):
    pass


class RuntimeException(DynamicException):
    """Base exception for Gobstones runtime errors."""

    def error_type(self):
        "Description of the exception type."
        return t('Runtime error')

class BoardCommandException(RuntimeException):

    def error_type(self):
        "Description of the exception type."
        return t('Board command error')


class BoardMoveException(BoardCommandException):

    def __init__(self, direction, area):
        super(BoardMoveException, self).__init__(['Cannot move to %s', (direction,)], area)





class ExceptionInterpretation:

    def __init__(self, messages, solutions=[]):
        self.messages = messages
        self.solutions = solutions
        self.solutions.insert(0, 'find_error_position')


INTERPRETATIONS = {
    'NameError' : ExceptionInterpretation([
        "name '{}' is not defined",
        "global name '{}' is not defined",
        ],
        [
            'check_value_name',
            'check_identifier_name',
            'check_variable_defined',
            'check_main_def'
        ]
    ),
    'IndentationError' : ExceptionInterpretation(
        [ 'unexpected indent' ],
        [
            'check_indent'
        ]
    ),
    'SyntaxError': ExceptionInterpretation(
        [ 'invalid syntax' ],
        [
            'check_syntax',
            'check_strange_character'
        ]),
    'BoardMoveException' : ExceptionInterpretation(
        [ 'Cannot move to {}' ],
        [
            'check_move',
            'check_command_order',
            'check_repetition',
            'check_precondition'
        ]),
    'BoardTakeStoneException' : ExceptionInterpretation(
        [ 'Cannot take stones of color {}' ],
        [
            'check_command_order',
            'check_repetition',
            'check_precondition'
        ])
}

def extract_message(e):
    return e.message

def interpretation(e):
    exception_type = e.error_class()
    out = ''
    if exception_type in INTERPRETATIONS.keys():
        message = extract_message(e)
        interpretation = INTERPRETATIONS[exception_type]
        interp = interpretation.messages
        result = None
        i = 0
        while i < len(interp) and result is None:
            result = parse(interp[i], message)
            i += 1
        if result is not None:
            out += t(interp[0])
            for r in result:
                out = out.format(t(r))

        out += '\n\n'

        out += t('to_fix_this_error') + ':\n'
        for solution in interpretation.solutions:
            out += '  - ' + t(solution) + '\n'

    return out

def to_message(filepath, e):
    if filepath is None:
        filepath = t('main program')

    ind = '  '
    out = []

    out.append(t('Error') + ':')
    out.append(e.area.replace('<string>', filepath).replace('\n', '\n'))
    out.append(ind + e.error_class() + ': ' + e.i18n_message)
    out.append('')

    message = interpretation(e)
    if message != '':
        out.append(t('Error interpretation') + ':')
        out.append(ind + message.replace('\n', '\n' + ind))
        out.append('')


    return '\n'.join(out)
