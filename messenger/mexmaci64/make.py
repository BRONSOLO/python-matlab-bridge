#!/usr/bin/python

import os
import sys
import fnmatch
import subprocess

# Check the system platform first
platform = sys.platform
print "This is a " + platform + " system"

# Open the configure file and start parsing
config = open('local.cfg', 'r')

for line in config:
    path = line.split('=')

    if path[0] == "MATLAB_BIN":
        print "Searching for Matlab bin folder in local.cfg ..."
        matlab_bin = path[1].rstrip('\r\n')
        if matlab_bin == "":
            raise ValueError("Could not find Matlab bin folder. Please add it to local.cfg")
        print "Matlab found in " + matlab_bin

    elif path[0] == "HEADER_PATH":
        print "Searching for zmq.h in local.cfg ..."
        header_path = path[1].rstrip('\r\n')
        if header_path == "":
            raise ValueError("Could not find zmq.h. Please add its path to local.cfg")
        print "zmq.h found in " + header_path

    elif path[0] == "LIB_PATH":
        print "Searching for zmq library in local.cfg ..."
        lib_path = path[1].rstrip('\r\n')
        if lib_path == "":
            raise ValueError("Could not find zmq library. Please add its path to local.cfg")

	print "zmq library found in " + lib_path

config.close()

# Get the extension
if platform == 'win32':
    extcmd = '"' + matlab_bin + "\\mexext.bat" + '"'
    check_extension = subprocess.Popen(extcmd, stdout = subprocess.PIPE)
    extension = check_extension.stdout.readline().rstrip('\r\n')
else:
    extcmd = matlab_bin + "/mexext"
    check_extension = subprocess.Popen(extcmd, stdout = subprocess.PIPE)
    extension = check_extension.stdout.readline().rstrip('\r\n')

print "Building messenger." + extension + " ..."

# Build the mex file
if platform == 'win32':
    mex = "\\mex.bat"
else:
    mex = "/mex"
make_cmd = '"' + matlab_bin + mex + '"' + " -O -I" + header_path + " -L" + lib_path + " -lzmq ../src/messenger.c"
os.system(make_cmd)

