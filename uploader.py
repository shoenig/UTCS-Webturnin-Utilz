#!/usr/bin/env python
# upload grades.txt to UTCS Webturnin
# Seth Hoenig 2012 (seth.a.hoenig@gmail.com)

import os
import random

def get_login_info():
    usrnm = raw_input('UTCS Username: ')
    passwd = raw_input('UTCS Password: ')
    course = raw_input('Course: ')
    assin = raw_input('Assignment #: ')
    return (usrnm, passwd, course, assin)

def login(usrnm, passwd):
    cmd = 'curl -c cookies.txt ' + \
        '-d \"username=' + usrnm + '\" ' + \
        '-d \"password=' + passwd + '\" ' + \
        '"http://turnin.microlab.cs.utexas.edu/turnin/webturnin.dll/login"'

    print 'cmd: %s' % cmd
    os.system(cmd)

# return a random happy comment
# def happy_comment():
#     phrases = ['Good Job!', 'Excellent Work!', 'Neato!']
#     return phrases[random.randint(0, len(phrases)-1)]

# read grades.txt and return a list of records
# a record is a tuple in the form: (utcsname, comment)
def slurp_grades():
    with open('./grades.txt') as gradesf:
        records = []
        for line in gradesf.readlines():
            sp = line.split()
            account = sp[1]
            # you could replace '' with happy_comment()
            comment = '' if len(sp) < 3 else \
                reduce(lambda x,y: x+y, sp[2:]) # && cat /dev/lololol
            records.append( (account, comment) )
        return records

url = 'http://turnin.microlab.cs.utexas.edu/turnin/webturnin.dll'
def upload_comments(u, p, c, a):
    for record in slurp_grades():
        # make an A#.txt file in /tmp for every comment file
        with open('/tmp/A' + a + '.txt', 'w') as tempf:
            print record
            print >>tempf, record[1]
            # magical upload part
            cmd = 'curl -F \"class=' + c + '\" ' + \
                '-F \"user=' + record[0] + '\" ' + \
                '-F \"file=/tmp/A' + a + '.txt;filename=A' + a + '.txt '+ \
                '-b cookies.txt -c cookies.txt ' + \
                '\"' + url + '\" '
            print cmd + '\n'
                

if __name__ == '__main__':
    u, p, c, a = get_login_info()
#    login(u, p)
    upload_comments(u, p, c, a)
