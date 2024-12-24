from uuid import uuid4

def code_generator() -> int:
    """
        Tasodifiy sonlar generatsiya qiladi
    """
    return int(str(uuid4().int)[:14])
