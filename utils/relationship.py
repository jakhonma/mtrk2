def add_many_to_many(obj, obj_list):
    """
        Informationga (mtv, region, language, format) larni qushish
    """
    for item in obj_list:
        obj.add(item)


def edit_many_to_many(obj, obj_list):
    """
        Informationga (mtv, region, language, format) larni o'zgartirish
    """
    if obj_list is not None:
        obj.set(obj_list)