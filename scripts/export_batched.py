#!/usr/bin/env python
import sys
import getpass
import subprocess
from time import sleep
import argparse
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

parser = argparse.ArgumentParser(
    description='Export content from a plone site')
parser.add_argument('--zopeclient',
                    required=True,
                    help='Path to zope client script (e.g. ./bin/instance)')
parser.add_argument('--ploneurl',
                    required=True,
                    help='URL to plone (e.g. http://localhost:8080/Plone)')
parser.add_argument('--meta_type',
                    default='',
                    help='meta_type to export (e.g Document)')
parser.add_argument('--path',
                    default='',
                    help='path to export (e.g. /plone/news)')
parser.add_argument('--total',
                    required=True,
                    type=int,
                    help='Total number of items to export')
parser.add_argument('--b_size',
                    required=True,
                    type=int,
                    help='Batch size')
parser.add_argument('--output',
                    required=True,
                    help='Output directory (must already exist)'
                    ' and be writeable by zope.')
args = parser.parse_args()

if not (args.path or args.meta_type):
    print "Please provide either path or meta_type"
    sys.exit(1)

print 'Trying to reindex %s of type %s%s (batch size %s)' % (
    args.total,
    args.meta_type or '(All)',
    args.path and ' in path %s' % args.path or '',
    args.b_size)

user = raw_input(
    "Username [%s] (You should input"
    " the admin zope user): " % getpass.getuser())
if not user:
    user = getpass.getuser()
pw = getpass.getpass()
auth = (user, pw)

b_start = 0
while b_start < args.total:
    print 'Processing items %s to %s' % (b_start+1, b_start+args.b_size+1)
    print 'Starting zope'
    subprocess.call([args.zopeclient, 'start'])
    print 'Waiting for zope...'
    sleep(15)
    url = '%s/@@export?meta_type=%s&path=%s&b_size=%s&b_start=%s&export_dir=%s' % (
        args.ploneurl,
        args.meta_type,
        args.path,
        args.b_size,
        b_start,
        args.output)
    print 'Loading', url
    r = requests.get(url, auth=auth)

    print 'Stopping zope'
    subprocess.call([args.zopeclient, 'stop'])
    b_start += args.b_size

print 'Done'
