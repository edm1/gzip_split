#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Ed Mountjoy
#

import os
import argparse
import gzip
from math import ceil
from itertools import islice

def main():

    # Args
    global args
    args = parse_args()

    # Calculate number of lines per split
    lines = count_lines(args.inf, args.header, args.comment)
    lines_per_split = ceil(float(lines) / args.chunks)
    assert lines >= args.chunks, 'Number of lines is less than --chunks'

    with gzip.open(args.inf, 'r') as in_h:

        # Skip comment lines
        for line in in_h:
            if args.comment and line.decode().startswith(args.comment):
                continue
            else:
                # Save first line
                first_line = line
                break

        # Get header
        if args.header == 'no_header':
            header = None
        else:
            header = first_line
            first_line = None

        # Write in chunks
        chunk_n = 0
        while True:

            # Create output file
            out_name = args.out_pattern.format(str(chunk_n).zfill(
                len(str(args.chunks - 1))))

            with gzip.open(out_name, 'w') as out_h:

                # Write header
                if (header and (
                    ((args.header == 'first') and chunk_n == 0) or
                    (args.header == 'all'))):
                    out_h.write(header)

                # Write first line and get remaining
                if first_line is None:
                    next_n_lines = islice(in_h, lines_per_split)
                else:
                    out_h.write(first_line)
                    next_n_lines = islice(in_h, lines_per_split - 1)

                # Write remaining lines
                for line in next_n_lines:
                    out_h.write(line)

            # Break if EOF
            first_line = in_h.readline()
            if not first_line:
                break

            chunk_n += 1

    # Delete original
    if args.delete:
        os.remove(args.inf)

    return 0

def count_lines(inf, header=None, comment=None):
    ''' Counts the total number of line in input, not including comments or
        header
    Params:
        inf (str): input file
        header (bool): whether the file contains a header
        comment (str): skip lines starting with this character
    Returns:
        int
    '''
    if comment:
        comment_bytes = comment.encode()
    c = 0
    # Count
    with gzip.open(inf, 'r') as in_h:
        for line in in_h:
            # Skip comment lines
            if comment is not None and line.startswith(comment_bytes):
                continue
            c += 1
    # Subtract header
    if header is not None:
        c = c - 1
    return c

def parse_args():
    """ Load command line args
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('--inf', metavar="<file>", help=('Input gzip file'), type=str, required=True)
    parser.add_argument('--out_pattern', metavar="<str>", help=('Output pattern, using "{}" as a wildcard. If not specified, will use input path.'), type=str, required=False)
    parser.add_argument('--chunks', metavar="<int>", help=('Number of chunks to split into'), type=int, required=True)
    parser.add_argument('--comment', metavar="<str>", help=('Skip lines at top of file that start with this character'), type=str)
    parser.add_argument('--delete', help=('Deletes the source file upon successful completion'), action='store_true')
    parser.add_argument('--header',
                        help=(
                            "Header mode:\n"
                            " (a) no_header, the input does not contain a header"
                            " (b) first, copy the header to the first split only"
                            " (c) all, copy the header to all splits"
                            " (d) none, don't copy header to any splits"
                        ),
                        choices=['no_header', 'first', 'all', 'none'],
                        type=str, required=True)
    args = parser.parse_args()

    # Create output pattern if not specified
    if not args.out_pattern:
        args.out_pattern = args.inf.replace('.gz', '.split{}.gz')
    assert '{}' in args.out_pattern, '--out_pattern must contain a wildcard {}'

    return args

if __name__ == '__main__':
    main()
