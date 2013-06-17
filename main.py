import sys

import argparse

from parse import do_parse

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
            description='crass: a CSS3 utility')
    parser.add_argument(
            'input', metavar='path', nargs='?',
            help='The path to the file to minify')
    parser.add_argument(
            '--pretty', action='store_const', const=True, default=False,
            help='Pretty print the parsed CSS')
    parser.add_argument(
            '--optimize', action='store_const', const=True, default=False,
            help='Optimize parsed CSS')
    args = parser.parse_args()

    if args.input:
        with open(args.input) as inp:
            stylesheet = do_parse(inp.read())
    else:
        stylesheet = do_parse(sys.stdin.read())

    if args.optimize:
        stylesheet = stylesheet.optimize()
    if args.pretty:
        sys.stdout.write(stylesheet.pretty())
    else:
        sys.stdout.write(unicode(stylesheet))

