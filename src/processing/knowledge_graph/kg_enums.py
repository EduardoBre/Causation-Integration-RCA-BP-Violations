from enum import Enum, auto


class Relationships(Enum):
    """
    ENUMS for the identification of relationship-types between two nodes.
    """
    DIRECTLY_FOLLOWS = 'directly follows'
    EVENTUALLY_FOLLOWS = 'eventually follows'


class KGType(Enum):
    """
    ENUMS for the identification of KG-types.
    """
    GENERIC = auto()
    EVENT_KG = 'Event Knowledge Graph'
    CONSTRAINT_KG = auto()


class NodeType(Enum):
    """
    ENUMS for the identification of Node-types.
    """
    GENERIC = auto()
    EVENT = 'Event'
