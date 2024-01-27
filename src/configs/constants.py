from enum import Enum


class SortDirection(Enum):
    ASC = 'asc'
    DESC = 'desc'


class SortField(Enum):
    UPDATED_AT = 'updated_at'
    VIEWS = 'views'
