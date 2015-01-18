#!/usr/bin/env python
# encoding: utf-8

import sys
import re
import argparse
from operator import itemgetter

COMMENT_CHAR = '#'

def print_separator():
    print("=" * 70)

def simple_diff(set1, set2, fmt):
    result = [(set1[line], line) for line in set(set1.keys()) - set(set2.keys())]

    for idx, line in sorted(result, key=itemgetter(0)):
        print(fmt.format(idx=idx, line=line))

def diff(set1, set2, numbering=True):
    if numbering:
        import math
        max_val = max([x for x in list(set1.values()) + list(set2.values())])
        digits = int(math.log10(max_val))+1
        fmt_idx = " {idx:0%dd}: {line:s}" % digits
    else:
        fmt_idx = " {line:s}"

    print_separator()

    fmt = "<" + fmt_idx
    simple_diff(set1, set2, fmt)

    print_separator()

    fmt = ">" + fmt_idx
    simple_diff(set2, set1, fmt)

    print_separator()

def scan_file(fname, comment):
    """Scans the configuration file ignoring comments.

    :fname: The filename
    :comment: The character preceding a comment
    :returns: A set with the functional lines in the configuration file

    """

    f = open(fname, 'r')

    contents = {}
    comment_re = re.compile(r"^\s*%s" % comment)

    for idx, line in enumerate(f.readlines()):
        if comment_re.match(line):
            continue

        line = line.strip()

        if line:
            # We don't care about duplicates, just keep one
            contents[line] = idx + 1

    f.close()
    return contents

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-c',
        '--comment',
        type=str,
        default=COMMENT_CHAR,
        action='store',
        help='the character preceding a comment (default: %s)'
        % COMMENT_CHAR)

    parser.add_argument(
        '--numbers',
        dest='numbers',
        action='store_true',
        help="show numbering (default: true)")

    parser.add_argument(
        '--no-numbers',
        dest='numbers',
        action='store_false',
        help="don't show numbering (default: false)")

    parser.set_defaults(numbers=True)

    parser.add_argument('file1', type=str, default=None, help='The first file')
    parser.add_argument('file2', type=str, default=None, help='The second file')

    args, unknown = parser.parse_known_args()

    if len(unknown):
        print("Unknown argument(s): %r" % unknown)
        parser.print_help()
        sys.exit(-1)

    try:
        contents1 = scan_file(args.file1, args.comment)
        contents2 = scan_file(args.file2, args.comment)
    except Exception as e:
        print(e)
        sys.exit(-1)

    if set(contents1.keys()) == set(contents2.keys()):
        print("They are equivalent")
        sys.exit(0)

    diff(contents1, contents2, args.numbers)


