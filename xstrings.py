#!/usr/bin/env python2

'''
xstrings - print the strings of encoded printable characters in files.
inspired by 'xorsearch' by didier stevens, http://blog.didierstevens.com/programs/xorsearch

@author Eli Cohen-Nehemia, https://github.com/elicn/xstrings
'''

import re
import argparse

from string import printable
from sys import stdin

PROG_NAME = 'xstrings.py'
PROG_DESC = 'Display printable strings in [file(s)] (stdin by default)'

def encoding(func):
    '''
    Wrapper method that constructs an encoded charmap according to given single-char encoding
    function.

    @param  func    Encoding function that accepts a single character and a key value

    @return A function for constructing a charmap
    '''

    def wrapped(charset, key):
        return ''.join('%c' % func(ord(char), key) for char in charset)

    return wrapped

# aggregate a few standard encoding functions along with the range of values (keys) they operate on.
# each entry in the dictionary consists of a function to encode a single character and its keys range
#
# by default the encoders dictionary encloses:
#   xor - bitwise xor of every character in charmap with the current key; keys range is [1, 255]
#   ror - bitwise rotate-right every character in charmap by 'key' places; keys range is [1, 7]
#   shl - bitwise shift-left every character in charmap by 'key' places; keys range is [1, 4]
#   add - binary add 'key' value to evey character in charmap; keys range is [1, 133]

encoders = {'XOR' : (encoding(lambda char, key: char ^ key),                                 xrange(1, 256)),
            'ROR' : (encoding(lambda char, key: (char << (8 - key)) & 0xff | (char >> key)), xrange(1, 8)),
            'SHL' : (encoding(lambda char, key: (char << key) & 0xff),                       xrange(1, 5)),
#           'SHR' : (encoding(lambda char, key: (char >> key) & 0xff),                       xrange(1, 8))
            'ADD' : (encoding(lambda char, key: (char + key) % 0x100),                       xrange(1, 134))}

# required to support --use-encoding command line option
class filter_dict(argparse.Action):
    '''A helper Action class that filters a dictionary according to a list of keys specified by the user
    and returns a subset dictionary. Option must specify 'default' and assign the dictionary to filter.

    @sa argparse.Action
    '''

    def __call__(self, parser, namespace, values, option_string):
        unfiltered = self.default
        filtered = dict((k, unfiltered.get(k)) for k in values if unfiltered.has_key(k))

        setattr(namespace, self.dest, filtered)

# required to support --use-encoding command line option
def comma_list(val):
    '''A helper function for separating string elements delimited by commas into a list of strings.
    For exmaple: comma_list('A,B,C,D') results in: ['A', 'B', 'C', 'D']
    '''

    return val.split(',')

# required to support --use-encoding command line option
class xlist(list):
    '''A helper class to support multi-choice in argparse module.
    For a list L and xlist XL, the expression 'L in XL' will return True iff XL contains all elements in L
    '''

    def __contains__(self, keys):
        return all(list.__contains__(self, k) for k in keys)

def finditer(content, encodings, charset, min_size):
    '''Generator function that iterates over all string matches inside the given content which are at least
    min_size characters long.

    @param    content    Binary content to search in
    @param    encodings  Dictionary of encoding functions
    @param    charset    An interable object containing the characters to consider as part of a string
    @param    min_size   Minimal string size to consider as a string match

    @return A tuple containing the match offset in content, encoding name, encoding key and the deobfuscated
            string reconstructed from the blob found
    '''

    # iterate over available encoding fucntions
    for encoding_name, (encoding_function, encoding_range) in encodings.items():

        # iterate over all keys in range for that encoding function
        for key in encoding_range:
            encoded_charset = encoding_function(charset, key)

            pattern = '[%s]{%d,}' % (re.escape(encoded_charset), min_size)

            for match in re.finditer(pattern, content):
                # deobfuscation: reconstruct the original string
                deobf = ''.join(charset[encoded_charset.index(c)] for c in match.group(0))

                yield (match.start(0), encoding_name, key, deobf)

        # cleanup regex cache once in a while
        re.purge()

def main(args):
    # prepare the format string for file offsets if required
    if args.radix:
        radixfmt = '%%7%s' % args.radix

    # iterate over input files list
    for fd in args.infiles:

        # gnu strings emits '{standard input}' instead of 'stdin' if required to emit filename
        # stick with the snu strings style if necessary
        if args.print_file_name:
            filename = '{standard input}' if fd == stdin else fd.name

        # iterate over findings in current input file
        # each iteration returns offset, encoding name, encoding key and deobfuscated string found
        for offset, enc_name, enc_key, deobf in finditer(fd.read(), args.encodings, args.charset, args.bytes):
            if args.print_file_name:
                print '%s:' % filename,

            if args.radix:
                print radixfmt % offset,

            print '%s(%x) %s' % (enc_name, enc_key, deobf)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog = PROG_NAME, description = PROG_DESC)

    parser.add_argument('-f', '--print-file-name', action = 'store_true', help = 'Print the name of the file before each string')
    parser.add_argument('-n', '--bytes',     type = int, default = 4, metavar = 'number', help = 'Locate & print any sequence of at least [number] characters')
    parser.add_argument('-t', '--radix',     type = str, choices = ('o', 'd', 'x'), help = 'Print the location of the string in base 8, 10 or 16')
    parser.add_argument('-c', '--charset',   type = str, default = printable, help = 'Replace the default characters set to look for with a custom one')
    parser.add_argument('-e', '--encodings', type = comma_list, action = filter_dict, choices = xlist(encoders), default = encoders, help = 'Encodings list to try out (default: all)')
    parser.add_argument('infiles', type = argparse.FileType('rb'), default = (stdin,), metavar = 'file', nargs = '*')

    main(parser.parse_args())
