# Utility class for grading stuff


# return a random happy comment
def happy_comment():
    phrases = ['Good Job!', 'Excellent Work!', 'Neato!']
    return phrases[random.randint(0, len(phrases)-1)]

def join_comment(splitted):
    return '' if len(splitted) < 4 else \
        reduce(lambda x,y: x+' '+y, splitted[3:])

def format_record(utcs, eid, missing_files, cmt='', grd=''):
    utcs_filler = ((' ' * (15 - len(utcs))))
    eid_filler = ((' ' * (15 - len(eid))))
    if not grd:
        grd = '00/20' if missing_files else '##/20'

    if missing_files:
        cmt = 'Missing File[s]: %s' % str(missing_files)
        return '%s   %s  %s %s %s %s' % \
            (grd, utcs, utcs_filler, eid, eid_filler, cmt)
    else:
        return '%s   %s  %s %s %s %s' % \
            (grd, utcs, utcs_filler, eid, eid_filler, cmt)
