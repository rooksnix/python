#! /usr/bin/python
#
# Given a list of kernel modules, print the device names they support
#
# KNOWN LIMITATIONS:
# * PCI devices only, no USB etc. yet.
# * Based on PCI (Sub)Vendor ID and (Sub)Device ID only. Baseclass ID, Subclass
#   ID, Interface information are effectively ignored for now.
# * Tested on RHEL6 only.

import sys
from subprocess import Popen
from subprocess import PIPE
import re
import os
import logging

logging.basicConfig()
log = logging.getLogger('hwlist')
log.setLevel(logging.CRITICAL)
#log.setLevel(logging.DEBUG)

def main():
    args = sys.argv[1:]

    if not args:
        log.error("Usage: %s module [module ...]" % sys.argv[0])
        sys.exit(1)

    # Step 1: read the PCI ID database

    # (sub)vendor ID -> name
    vendor = {}
    # vendor ID -> device ID -> name
    device = {}
    # vendor ID -> device ID -> subvendor ID -> subdevice -> subsystem_name
    subdevice = {}

    commentpattern = re.compile(r'\s*#')
    emptypattern = re.compile(r'^\s*$')
    vendorpattern = re.compile(r'^([0-9a-fA-F]{4})\s*(.*)$')
    devicepattern = re.compile(r'^\t([0-9a-fA-F]{4})\s*(.*)$')
    subdevicepattern = re.compile(r'^\t\t([0-9a-fA-F]{4})\s*([0-9a-fA-F]{4})\s*(.*)$')
    f = open('/usr/share/hwdata/pci.ids')
    for line in f:
        line = line.rstrip('\n')
        if re.match(commentpattern, line):
            continue
        matches = re.search(emptypattern, line)
        if matches:
            continue
        matches = re.search(vendorpattern, line)
        if matches:
            (vendorid, vendorname) = matches.groups()
            vendorid = vendorid.lower().zfill(8)
            vendor[vendorid] = vendorname
            device[vendorid] = {}
            continue
        matches = re.search(devicepattern, line)
        if matches:
            (deviceid, devicename) = matches.groups()
            deviceid = deviceid.lower().zfill(8)
            device[vendorid][deviceid] = devicename
            continue
        matches = re.search(subdevicepattern, line)
        if matches:
            (subvendorid, subdeviceid, subsystemname) = matches.groups()
            subvendorid = subvendorid.lower().zfill(8)
            subdeviceid = subdeviceid.lower().zfill(8)
            if not vendorid in subdevice:
                subdevice[vendorid] = {}
            if not deviceid in subdevice[vendorid]:
                subdevice[vendorid][deviceid] = {}
            if not subvendorid in subdevice[vendorid][deviceid]:
                subdevice[vendorid][deviceid][subvendorid] = {}
            subdevice[vendorid][deviceid][subvendorid][subdeviceid] = subsystemname
            continue
        log.debug('Failed to parse line: "{0}"'.format(line))
    f.close()

    # Step 2: read the driver's info and translate it

    pcidriver={}
    aliaspattern = re.compile(r'^alias:\s+(.*)$')
    #pcipattern = re.compile(r'pci:v([0-9a-fA-F]{8})d([0-9a-fA-F]{8}).*')
    pcipattern = re.compile(r"""
        pci:
        v([0-9a-fA-F]{8})       # Vendor ID
        d([0-9a-fA-F]{8})       # Device ID
        sv(\*|[0-9a-fA-F]{8})   # Subvendor ID
        sd(\*|[0-9a-fA-F]{8})   # Subdevice ID
        bc(\*|[0-9a-fA-F]{2})   # Baseclass ID
        sc(\*|[0-9a-fA-F]{2})   # Subclass ID
        i(.+)                   # Interface
    """, re.VERBOSE)
    for arg in args:
        basename = os.path.basename(arg)

        # Meh, Python 2.6 doesn't have subprocess.check_output yet
        out = Popen(['/sbin/modinfo', arg], stdout=PIPE).communicate()[0]
        for line in out.splitlines():
            matches = re.search(aliaspattern, line)
            if not matches:
                continue
            alias = matches.group(1)
            log.debug('Processing alias "{0}"'.format(alias))
            matches = re.search(pcipattern, alias)
            if not matches:
                # USB aliases etc. Not supported yet.
                log.warning('Don\'t know how to parse alias "{0}"; ignoring'.format(alias))
                continue
            (vendorid, deviceid,
             subvendorid, subdeviceid,
             baseclassid, subclassid, interface) = matches.groups()
            vendorid = vendorid.lower()
            deviceid = deviceid.lower()
            subvendorid = subvendorid.lower()
            subdeviceid = subdeviceid.lower()
            baseclassid = baseclassid.lower()
            subclassid = subclassid.lower()
            interface = interface.lower()
            if not vendorid in pcidriver:
                pcidriver[vendorid] = {}
            pcidriver[vendorid][deviceid] = basename

            vendorname = '[UNKNOWN]'
            devicename = '[UNKNOWN]'
            subvendorname = '[UNKNOWN]'
            if subvendorid == '*':
                subvendorname = '[ANY]'
            if subvendorid in vendor:
                subvendorname = vendor[subvendorid]
            subdevicename = '[UNKNOWN]'
            if subdeviceid == '*':
                subdevicename = '[ANY]'
                
            if vendorid in vendor:
                vendorname = vendor[vendorid]
            if vendorid in device and deviceid in device[vendorid]:
                devicename = device[vendorid][deviceid]
            if vendorid in subdevice and \
                deviceid in subdevice[vendorid] and \
                subvendorid in subdevice[vendorid][deviceid] and \
                subdeviceid in subdevice[vendorid][deviceid][subvendorid]:
                    subdevicename = subdevice[vendorid][deviceid][subvendorid][subdeviceid]
            
            print '{0} supports {1}:{2}:{3}:{4} == "{5}":"{6}":"{7}":"{8}"'.format(
                basename,
                vendorid, deviceid,
                subvendorid, subdeviceid,
                vendorname, devicename, subvendorname, subdevicename
            )
    
if __name__ == '__main__':
    main()

# vim: autoindent tabstop=4 expandtab smarttab shiftwidth=4 softtabstop=4 tw=0
