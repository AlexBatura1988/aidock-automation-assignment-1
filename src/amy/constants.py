from enum import Enum

COMPANY_DOMAIN = 'company.com'
VENDOR_DOMAINS = ['vendor1.com', 'vendor2.org']  # we can add the list of vendors here

HIGH_NUM_OF_FILES_THRESHOLD = 10
LOW_NUM_OF_FILES_THRESHOLD = 5

PRIORITY_PREFIX = 'priority:'


class Priority(Enum):
    high = 'high'
    medium = 'medium'
    low = 'low'

    @classmethod
    def from_str(cls, label):
        try:
            return cls(label)
        except:
            return cls.low


PRIORITY_TO_SCORE = {
    Priority.high: 1,
    Priority.medium: 2 / 3,
    Priority.low: 1 / 3
}
DEFAULT_PRIORITY_SCORE = 1 / 3
