#!/usr/bin/env python
# create a file called "grades.txt" which sets one up for quick
# grading and comment uploading. the format of grades.txt is:
#      grade/20  --utcsname----- Comments
# and can be uploaded to UTCS Webturnin using uploader.py
# Seth Hoenig 2012 (seth.a.hoenig@gmail.com)

import os
import shutil

keeplist = ['a.py']
pushlist = ['key.txt']

# delete everything except files listed in keeplist, so it's easier to
# see what we care about in the directory. keep in mind, files turned in
# with the wrong name will be deleted (just locally, of course)
def purge():
    for d, _, files in os.walk('./'):
        odir = d
        for f in files:
            if not f in keeplist:
                if(odir is not './'):
                    os.remove(odir + '/' + f)

# create a copy of each file in pushlist in each students directory
# for example, a common test case file, or data file
def push():
    cdir = './'
    for _, dirs, _ in os.walk(cdir):
        for dname in dirs:
            for item in pushlist:
                target = cdir + dname + '/' + item
                shutil.copy2('./' + item, target)


# grab all the user names from the folders, and put them in a text file
# with other info. if the user does not have one or more of the files
# in the keeplist, give them a grade of 0 (this will show up in the
# grade/comment file)
def setup_grade_file(wantedList=None):
    with open('./grades.txt', 'w') as fgrades:
        for d, _, files in os.walk('./'):
            if d is not './':
                odir = d
                missing = []
                for item in keeplist:
                    if item not in files:
                        missing.append(item)
                filler = ((' ' * (15 - len(d))))
                if missing:
                    message = 'Missing File[s]: %s' % str(missing)
                    print >>fgrades, '00/20   %s %s %s' % \
                        (str(d)[2:], filler, message)
                else:
                    print >>fgrades, '##/20   %s %s ' % \
                        (str(d)[2:], filler)
                

# program begins here
if __name__ == '__main__':
    purge()
    push()
    setup_grade_file()
        
