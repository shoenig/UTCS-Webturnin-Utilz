#!/usr/bin/env python
import datetime
import os
import subprocess
import time
import re

from assignments import assis

BASE_URL = 'https://turnin.microlab.cs.utexas.edu/turnin/webturnin.dll/'
UP_URL = BASE_URL + 'upload'
LOGIN_URL = BASE_URL + 'do_login'
HOME_URL = BASE_URL + 'home'

def is_late(html, asiname, duedate):
    duedate = fix_date(duedate)
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

def get_login_info():
    """Ask for and return a tuple of login information"""
    usrnm = raw_input('UTCS Username: ')
    passwd = raw_input('UTCS Password: ')
    course = raw_input('Course: ')
    return (usrnm, passwd, course)

def login(usrnm, passwd):
    """Login to UTCS Webturnin. This will create cookie.txt for later use."""
    cmd = 'curl -c cookies.txt ' + \
        '-d \"username=' + usrnm + '\" ' + \
        '-d \"password=' + passwd + '\" ' + \
        '--insecure ' + \
        '-H "Expect:" ' + \
        '\"' + LOGIN_URL + '\"'
    os.system(cmd + ' 2>/dev/null 1>/dev/null') # Popen doesn't work for some reason
    time.sleep(1)

def get_class_html(course):
    """Fetch the html of the home screen after logging in"""
    cmd = 'curl --insecure -b cookies.txt -c cookies.txt --url ' + HOME_URL + \
        '?class=' + course + '.GRADER'
    DEVNULL = os.open(os.devnull, os.O_RDWR)
    proc = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=DEVNULL)
    html = proc.stdout.read()
    return html

def get_student_list(html):
    std_re = 'option value="([\w]+)"[\W](selected)?>([\s\w\\,\\.]+)'
    idx = html.index('select name="user"')
    m = True
    recs = []
    while m is not None:
        m = re.search(std_re, html[idx:])
        if m is not None:
            recs.append( [m.group(1), m.group(3), 0] )
            idx = html.index(m.group(0)) + 1
    return recs

def process_student_list(course, studs, asmnts):
    for stud in [y for y in studs]:
        shtml = get_student_html(course, stud[0])
        r = process_student(shtml, asmnts)
#TODO: pretty format name
        print '%s %s' % (stud[0] + '-'*(14-len(stud[0])), stud[1])
        for item in r:
            print '\t\t\t%s: %r' % (item, r[item])

def get_student_html(course, user):
    cmd = 'curl --insecure -b cookies.txt -c cookies.txt --url ' + HOME_URL + \
        '?class=' + course + '.GRADER&user=' + user
    DEVNULL = os.open(os.devnull, os.O_RDWR)
    proc = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=DEVNULL)
    html = proc.stdout.read()
    return html

def process_student(html, assignments):
    """
    Look for lateness of each assignment in assignments dict. Return
    a dict {assiname:dayslate}.
    """
    results = {}
    for assi in assignments:
        lateness = None
        try:
            lateness = is_late(html, assi, assignments[assi])
            if lateness:
                results[assi] = lateness
        except ValueError:
            #results[assi] = None # a missing assignment, not actually useful info
            pass

    return results

if __name__ == '__main__':
    u, p, c = get_login_info()
    login(u, p)
    print ''
    h = get_class_html(c)
    slist = get_student_list(h)
    process_student_list(c, slist, assis)
