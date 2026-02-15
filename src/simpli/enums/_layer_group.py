from enum import IntEnum


class LayerGroup(IntEnum):
    BACKGROUND = -1
    GEOMETRY = 0
    LABELS = 1
    FOREGROUND = 2
    UI = 3
