#!/usr/bin/env python

# == ivMeta: Extract meta data from iPhone videos
#
# ivMeta will attempt to pull the following bits of information from an iPhone
# video:
#
# * Maker
# * iOS Software version
# * Date video was taken
# * GPS co-ords where video was taken
# * Model of phone
#
# It is designed from information given in the following CSI Tech blog:
#
# http://www.csitech.co.uk/iphone-video-metadata
#
# Example output
#
# ********************************
# Parsing: iphone.mov
# ********************************
# Type Marker: qt
# Maker: Apple
# Software version: 6.1
# Date: 2013-06-03T13:45:04+0000
# GPS: lat:+53.3831 long:-001.4600 dir:+076.540
# Model: iPhone 4
#
# == Usage
#
# ivMeta 1.0 Robin Wood (robin@digininja.org) (www.digininja.org)
#
# usage: ivmeta.py [-h] [-v] file.mov [file.mov ...]
#
# Parse metadata from an iPhone video
#
# positional arguments:
#   file.mov       Videos to analyse
#
# optional arguments:
#   -h, --help     show this help message and exit
#   -v, --verbose  Verbose output
#
# Author:: Robin Wood (robin@digininja.org)
# Copyright:: Copyright (c) Robin Wood 2013
# Licence:: Creative Commons Attribution-Share Alike 2.0
#

from struct import *
from pprint import pprint
import argparse
import sys

print """ivMeta 1.0 Robin Wood (robin@digininja.org) (www.digininja.org)
"""

parser = argparse.ArgumentParser(
    description="Parse metadata from an iPhone video"
)
parser.add_argument("filename",
                    metavar="file.mov", nargs="+", help="Videos to analyse"
                    )
parser.add_argument("-v", "--verbose",
                    dest="verbose", default=False,
                    action="store_true", help="Verbose output"
                    )
args = parser.parse_args()

verbose = args.verbose

if args.filename is None:
    print "You must provide a filename to parse"
    sys.exit(1)

for filename in args.filename:
    print ("********************************")
    print ("Parsing: " + filename)
    print ("********************************")

    try:
        f = open(filename, "rb")
    except IOError:
        print "Couldn't open the file\n"
        continue

    s = f.read()
    pos = s.find("ftyp")

    if pos > -1:
        len_tup = unpack("B", s[pos+5])
        str_len = len_tup[0]
        if verbose:
            print ("Type starts at " + str(pos) + " and ends at " +
                   str(pos + 8 + str_len) + " (length " + str(str_len) + ")")
        phone_type = (s[pos+4:pos + 4 + 4]).strip()

        print ("Type Marker: " + phone_type)
        if phone_type != "qt":
            print ("File doesn't appear to be an iPhone video\n")
            continue
    else:
        print("Type Marker: Not found")
        print ("File doesn't appear to be an iPhone video\n")
        continue

    pos = s.find("\xa9mak")

    if pos > -1:
        len_tup = unpack("B", s[pos+5])
        str_len = len_tup[0]
        if verbose:
            print ("+ Maker starts at " + str(pos) + " and ends at " +
                   str(pos + 8 + str_len) + " (length " + str(str_len) + ")")
        maker = s[pos+8:pos + 8 + str_len]

        print ("Maker: " + maker)
    else:
        print("Maker: Not found")

    pos = s.find("\xa9swr")

    if pos > -1:
        len_tup = unpack("B", s[pos+5])
        str_len = len_tup[0]
        if verbose:
            print ("+ Version starts at " + str(pos) + " and ends at " +
                   str(pos + 8 + str_len) + " (length " + str(str_len) + ")")
        version = s[pos+8:pos + 8 + str_len]

        print ("Software version: " + version)
    else:
        print("Software version: Not found")

    pos = s.find("\xa9day")

    if pos > -1:
        len_tup = unpack("B", s[pos+5])
        str_len = len_tup[0]
        if verbose:
            print ("+ Date starts at " + str(pos) + " and ends at " +
                   str(pos + 8 + str_len) + " (length " + str(str_len) + ")")
        date_str = s[pos+8:pos + 8 + str_len]

        print ("Date: " + date_str)
    else:
        print("Date: Not found")

    pos = s.find("\xa9xyz")

    if pos > -1:
        len_tup = unpack("B", s[pos+5])
        str_len = len_tup[0]
        if verbose:
            print ("+ GPS starts at " + str(pos) + " and ends at " +
                   str(pos + 8 + str_len) + " (length " + str(str_len) + ")")
        gps_all = s[pos+8:pos + 7 + str_len]
        gps_lat = gps_all[:8]
        gps_long = gps_all[8:17]
        gps_dir = gps_all[17:]

        print ("GPS: lat:" + gps_lat + " long:" + gps_long + " dir:" + gps_dir)
    else:
        print("GPS: Not found")

    pos = s.find("\xa9mod")

    if pos > -1:
        len_tup = unpack("B", s[pos+5])
        str_len = len_tup[0]
        if verbose:
            print ("+ Model starts at " + str(pos) + " and ends at " +
                   str(pos + 8 + str_len) + " (length " + str(str_len) + ")")
        model = s[pos+8:pos + 8 + str_len]

        print ("Model: " + model)
    else:
        print("Model: Not found")

    print
