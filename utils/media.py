from django.conf import settings
import os

def delete_media(file_name):
    paths = settings.MEDIA_ROOT
    os.remove(os.path.join(paths, file_name))