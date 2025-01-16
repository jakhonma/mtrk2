from django.utils import timezone
import pytz


def current_time_tashkent_now(letter):
    tashkent_tz = pytz.timezone('Asia/Tashkent')
    current_time_tashkent = timezone.now().astimezone(tashkent_tz)
    return current_time_tashkent
