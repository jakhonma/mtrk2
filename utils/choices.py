from enum import Enum


class UserRoleEnum(Enum):
    ADMIN = 'ADMIN'
    LEADER = 'LEADER'
    EMPLOYEE = 'EMPLOYEE'
    LOW_USER = 'LOW_USER'

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
