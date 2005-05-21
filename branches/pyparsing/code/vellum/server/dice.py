import sys
import random

def rollDie(die, mod=0):
    return random.choice(range(1, die+1)) + mod

def parseRange(odds):
    if '-' in odds:
        low,hi = odds.split('-')
    else:
        low = hi = odds
    return int(low), int(hi)

def choosePercentile(percentiles):
    """Utility function for choosing an item from a list formatted like this:
    ['01-11','13-73','74-99','100']
    Returns the index of the item selected from the list.
    """
    pctile = roll(100)
    for n, outcome in enumerate(percentiles):
        low,hi = parseRange(outcome)
        if low <= pctile <= hi:
            return n
    raise RuntimeError, "None of %s were selected" % (percentiles,)


def most(lst, count, direction=1):
    """Return the greatest <count> items in lst"""
    lst.sort()
    if direction == 1:
        lst.reverse()
    return lst[:count]

least = lambda l, c: most(l, c, -1)

def roll(parsed):
    # set these to defaults in the finish step, not in the init, 
    # so the parser instance can be reused
    import pdb; pdb.set_trace()
    identity = lambda l: l
    if parsed.dice_filter == None:
        parsed.dice_filter = identity
    if parsed.dice_size == '':
        # an int by itself is just an int.
        if (parsed.dice_count > 0 and parsed.dice_filter is identity):
            for n in xrange(parsed.dice_repeat):
                yield parsed.dice_count + parsed.dice_bonus
            return
        raise RuntimeError("Syntax error: No die size was given")
    for n in xrange(parsed.dice_repeat):
        tot = sum(parsed.dice_filter(
              [rollDie(parsed.dice_size, 0) for n in xrange(parsed.dice_count)]
                  ))
        tot = tot + parsed.dice_bonus
        yield tot


def test():
    for dice in ['d6xz',  # repeat not a number
                 '1d', # left out die size 
                 '1d6l3l3', '1d6h3l3',  # can't specify more than one filter
                 '1d6h+1', # can't leave the die count out of the filter
                 '1d6h2+1', # can't keep more dice than you started with
                 '', # empty should be an error
                 #'1d6+5 1d1' # FIXME, last one doesn't fail correctly
                 ]:
        try:
            roll(dice)
        except RuntimeError, e:
            print e
        else:
            assert 0, "%s did not cause an error, and should've" % (dice,)
    print roll('5')
    print roll('5x3')
    print roll('5+1x3')
    print roll('d6x3')
    print roll('9d6l3-10x2')
    print roll('9d6h3+10x2')
    print roll('1d  6 x3')
    print roll('d 6 -2 x 3')
    print roll('2d6-2x1')
    for n in xrange(1000):
        assert roll('5')[0] == 5
        assert roll('5x3')[2] == 5
        assert roll('5+1x3')[2] == 6
        assert 1 <= roll('d6')[0] <= 6
        assert 3 <= roll('3d6')[0] <= 18
        assert 2 <= roll('9d6l3-1x2')[0] <= 17
        assert 4 <= roll('9d6h3+1x2')[0] <= 19
        assert 1 <= roll('1d  6')[0] <= 6
        assert 3 <= roll('d6+2')[0] <= 8
        assert -1 <= roll('d 6 -2')[0] <= 4
        assert 4 <= roll('2d6+ 2')[0] <= 14
        assert 0 <= roll('2d6-2')[0] <= 10
    print 'passed all tests'

def run(argv=None):
    import linesyntax
    if argv is None:
        argv = sys.argv
    while 1:
        try:
            st = raw_input("Roll: ")
            parsed = linesyntax.dice.parseString(st)
            rolled = roll(parsed)
            if len(list(rolled)) > 1:
                print "Unsorted--", rolled
                rolled.sort()
                rolled.reverse()
                print "Sorted----", rolled
            else:
                print rolled[0]
        except RuntimeError, e:
            print e

if __name__ == '__main__':
    sys.exit(run())
