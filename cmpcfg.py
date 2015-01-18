#!/usr/bin/env python
# encoding: utf-8

import sys
import re
import argparse

COMMENT_CHAR = '#'

def print_separator():
    print("=" * 70)

def scan_file(fname, comment):
    """Scans the configuration file ignoring comments.

    :fname: The filename
    :comment: The character preceding a comment
    :returns: A set with the functional lines in the configuration file

    """

    f = open(fname, 'r')

    contents = []
    comment_re = re.compile(r"^\s*%s" % comment)

    for line in f.readlines():
        if comment_re.match(line):
            continue

        line = line.strip()

        if line:
            contents.append(line)

    f.close()
    return set(contents)

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

    if contents1 == contents2:
        print("They are equivalent")
        sys.exit(0)

    print_separator()

    for line in contents1 - contents2:
        print("< %s" % line)

    print_separator()

    for line in contents2 - contents1:
        print("> %s" % line)

    print_separator()


