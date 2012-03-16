from sdcounter import check_date
from sdcounter import fix_date
from sdcounter import compare_dates
from sdcounter import is_late


def test_check_date():
    assert check_date('03/29/1990')
    assert not check_date('3/29/1990')
    assert check_date('12/12/1934')
    assert not check_date('12/3/1934')
    assert not check_date('11/11/11')
    assert check_date('11/11/2011')

def test_fix_date():
    d = '03/04/2008'
    assert fix_date('03/04/2008') == d
    assert fix_date('3/04/2008') == d
    assert fix_date('03/4/2008') == d
    assert fix_date('3/4/2008') == d
    assert fix_date('03/04/08') == d
    assert fix_date('3/04/08') == d
    assert fix_date('03/4/08') == d
    assert fix_date('3/4/08') == d

def test_compare_dates():
    dA = '03/04/2008'
    dB = '03/05/2008'
    dC = '04/01/2008'

    assert compare_dates(dA, dB) == 1
    assert compare_dates(dB, dA) == -1
    assert compare_dates(dA, dC) == 28
    assert compare_dates(dC, dA) == -28

def test_is_late():
    with open('test.html', 'r') as f:
        html = f.read()
        res = is_late(html, 'Guess.py', '02/20/2012')
        assert res == None
        res = is_late(html, 'Fence.py', '02/13/2012')
        assert res == 1
        res = is_late(html, 'Fence.py', '02/15/2012')
        assert res == None


if __name__ == '__main__':
    test_check_date()
    test_fix_date()
    test_compare_dates()
    test_is_late()
    print 'tests done.'
