def report_info(report):
    lst = ''
    for item in report.reports.all():
        lst += item.name + '\n'

    print(lst)
    return lst
