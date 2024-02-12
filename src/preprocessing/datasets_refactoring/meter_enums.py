from enum import Enum, auto


class ReportStatus(Enum):
    """
    ENUMS for ALARM or EVENT ("LP Display OFF" or "LP Display ON")
    """
    ALARM = auto()
    EVENT = auto()


class SynchronizationStatus(Enum):
    """
    ENUMS for the status of the synchronization between the Central System and Meter
    """
    SYNCHRONIZED = auto()
    UNSYNCHRONIZED = auto()


class MeterViewStatus(Enum):
    """
    ENUMS for the status of the Display View
    """
    DISPLAY_ON = auto()
    DISPLAY_OFF = auto()

