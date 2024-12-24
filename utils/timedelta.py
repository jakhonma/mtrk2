def times(time_delta):
    if time_delta:
        total_seconds = int(time_delta.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours}:{minutes}:{seconds}"
    else:
        return "00:00:00"
