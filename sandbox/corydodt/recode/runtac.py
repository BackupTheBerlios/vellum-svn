from twisted.python.runtime import platformType

if platformType == 'win32':
    from twisted.scripts._twistw import run
else:
    from twisted.scripts.twistd import run

import sys
real_argv = sys.argv
sys.argv = ['twistd', '-noy', 'vr.tac']

run()
