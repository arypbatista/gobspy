from .enum import Enum
from ...i18n import translate as t

#### Colors

COLOR_NAMES = [
    'Color0',
    'Color1',
    'Color2',
    'Color3',
]

class Color(Enum):
    "Represents a Gobstones color."

    def enum_type(self):
        "Return the name of the enumerated type."
        return 'Color'

    def enum_size(self):
        "Return the size of the enumerated type."
        return 4

    def name(self):
        "Return the name of this color."
        return COLOR_NAMES[self.ord()]

    def __repr__(self):
        return self.name()


COLORS = [Color(i) for i in range(len(COLOR_NAMES))]

COLORS_BY_NAME = dict([(c.name(), c) for c in COLORS])

NUM_COLORS = len(COLORS)
