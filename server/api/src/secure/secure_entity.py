# classes for secure work

class Role:
    ADMIN = "A"
    MANAGER = "M"
    USER = "U"

ROLE_HIERARCHY = {
    Role.ADMIN: 3,
    Role.MANAGER: 2,
    Role.USER: 1,
}