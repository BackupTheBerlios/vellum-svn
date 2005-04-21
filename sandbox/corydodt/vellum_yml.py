"""
Copy this file to C:\pf\PCGen\vellum_yml.py
then set the standard output processor in preferences, to:
python C:\pf\PCGen\vellum_yml.py "%"

Features:
    - Inside single-quoted strings, replaces ' with '' so yaml can parse it
"""

import sys
import re


_re = re.compile("'(.+)'$")

def safeSingleQuotes(st):
    """Replace 'isn't' with 'isn''t'"""
    match = _re.search(st)
    if match is not None:
        replacement = "'%s'" % (match.group(1).replace("'", "''"),)
        return _re.sub(replacement, st)
    else:
        return st


def run(argv = None):
    if argv is None: argv = sys.argv
    if len(argv) != 2:
        print "usage: vellum_yml.py [filename]"
    filename = argv[1]
    output = []
    for line in file(filename):
        line = safeSingleQuotes(line)
        output.append(line)
    done = ''.join(output)
    file(filename, 'wb').write(done)

if __name__ == '__main__':
    sys.exit(run())
