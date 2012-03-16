#!/usr/bin/env python
import datetime

def is_late(html, asiname, duedate):
    assert check_date(duedate)
    idxA = html.index('>' + asiname) + 1
    idxBprime = html.index(',', idxA)
    idxB = idxBprime - 10
    turnindate = html[idxB:idxB+10]
    lateness = compare_dates(duedate, turnindate)
    if lateness > 0:
        return lateness
    return None

def compare_dates(dateA, dateB):
    assert check_date(dateA)
    assert check_date(dateB)
    dtA = datetime.datetime(int(dateA[-4:]), int(dateA[0:2]), int(dateA[3:5]))
    dtB = datetime.datetime(int(dateB[-4:]), int(dateB[0:2]), int(dateB[3:5]))
    daydelta = (dtB - dtA).days
    return daydelta
    
#Date needs to be EXACTLY in the form MM/DD/YYYY, implying
#there needs to be 10 characters in the correct format.
def fix_date(date):
    if len(date) > 10:
        raise Exception('too many characters in date', date)
    if check_date(date):
        return date
    if date.find('/') == 1:
        fixed = fix_date('0' + date)
        return fixed
    if date.index('/', 3) == 4:
        fixed = fix_date(date[0:3] + '0' + date[3:])
        return fixed
    if len(date[date.index('/',3)+1:]) == 2:
        temp = date[0:date.index('/',3)] + '/20' + date[-2:]
        fixed = fix_date(temp)
        return fixed

    raise Exception('poorly formatted date', date)


def check_date(date):
    if len(date) != 10:
        return False
    if date[2] != '/':
        return False
    if date[5] != '/':
        return False
    if int(date[0:2]) <= 0:
        return False
    if int(date[0:2]) > 12:
        return False
    return True

if __name__ == '__main__':
    pass
