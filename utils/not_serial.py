def not_serials(queryset):
    not_ = []
    if queryset.exists():
        all_serial = list(queryset.values_list('part', flat=True))
        for item in range(1, all_serial[-1] + 1):
            if item not in all_serial:
                not_.append(item)
        return not_
    else:
        return not_
