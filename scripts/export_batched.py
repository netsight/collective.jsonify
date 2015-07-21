#!/usr/bin/env python
import sys
import getpass
import subprocess
from time import sleep
try:
    import requests
except ImportError:
    print 'This script requires the requests library'
    print 'http://pypi.python.org/pypi/requests'
    sys.exit(1)

try:
    var = app
except NameError:
    pass
else:
    print 'This script should not be run as an instance script.'
    print 'Please run it as a simple python script'
    sys.exit(1)

if len(sys.argv) != 7:
    print 'Usage: %s zopeclient ploneurl meta_type total b_size export_dir' % sys.argv[0]
    sys.exit(1)

_, zopeclient, ploneurl, meta_type, total, b_size, export_dir = sys.argv
total = int(total)
b_size = int(b_size)

print 'Trying to reindex %s of type %s (batch size %s)' % (
    total, meta_type, b_size)

user = raw_input(
    "Username [%s] (You should input the admin zope user): " % getpass.getuser())
if not user:
    user = getpass.getuser()
pw = getpass.getpass()
auth = (user, pw)

b_start = 0
while b_start < total:
    print 'Processing items %s to %s' % (b_start+1, b_start+b_size+1)
    print 'Starting zope'
    subprocess.call([zopeclient, 'start'])
    print 'Waiting for zope...'
    sleep(15)
    url = '%s/@@export?meta_type=%s&b_size=%s&b_start=%s&export_dir=%s' % (
        ploneurl, meta_type, b_size, b_start, export_dir)
    print 'Loading', url
    r = requests.get(url, auth=auth)

    print 'Stopping zope'
    subprocess.call([zopeclient, 'stop'])
    b_start += b_size

print 'Done'
