from datetime import datetime
from dateutil.relativedelta import relativedelta


def school_start():
    now = datetime.now()
    then = datetime.strptime('2017-09-05 09:00:00', '%Y-%m-%d %H:%M:%S')

    difference = relativedelta(then, now)

    return("Fall Semester begins in **{}** months, **{}** days, **{}** hours, **{}** minutes and **{}**.**{}** seconds."
           " :thumbsup:"
           .format(
            str(difference.months),
            str(difference.days),
            str(difference.hours),
            str(difference.minutes),
            str(difference.seconds),
            str(difference.microseconds)
           ))
