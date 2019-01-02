from datetime import timedelta
import re

def get_duration_from_str(dur):
    dt = timedelta(0)
    components = dur.split('T')
    # if components.len == 1, then there is no time component
    if len(components) == 1:
        components = [components[0][1:], '']
    else:
        components[0] = components[0][1:]
    # if components.len == 2, and first component consists only of 'P', then there is no date component
    # otherwise, there are both date and time components

    #start with time component
    pieces = re.split('(\d+)',components[1])
    indx = len(pieces)-1
    while indx > 0:
        num = int(pieces[indx-1])
        if pieces[indx] == 'S':
            dt += timedelta(seconds=num)
        elif pieces[indx] == 'M':
            dt += timedelta(minutes=num)
        elif pieces[indx] == 'H':
            dt += timedelta(hours=num)
        indx -= 2

    #then do date component
    pieces = re.split('(\d+)',components[0])
    indx = len(pieces)-1
    while indx > 0:
        num = int(pieces[indx-1])
        if pieces[indx] == 'D':
            dt += timedelta(days=num)
        elif pieces[indx] == 'W':
            dt += timedelta(weeks=num)
        elif pieces[indx] == 'M':
            dt += timedelta(months=num)
        elif pieces[indx] == 'Y':
            dt += timedelta(years=num)
        indx -= 2
    return dt
