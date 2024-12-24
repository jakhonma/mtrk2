from django.utils import timezone
from uuid import uuid4

def directory_path(instance: str, filename: str):
    day = timezone.now()
    class_name = instance.__class__.__name__
    lst = filename.split('.')
    return f"{class_name}/{day.year}/{day.month}/{day.day}/{uuid4()}.{lst[-1]}"