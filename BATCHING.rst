For batch exporting, there is a utility python script that will try and
reduce memory usage as much as possible by batching the exports and
restarting zope in between.

It lives in scripts/export_batched.py if you have the egg checked out.
Otherwise copy it from github into your own project.

Usage:

export_batched.py [args]

Options:
zopeclient: path to zope startup script (e.g. ./bin/client)
ploneurl: url to plone (e.g. http://localhost:8080/Plone)
portal_type: the type of content to export
path: the path to export
total: total number of items to export (required for batching)
b_size: batch size
export_dir: directory to output the json files
            (must exist and be writeable by zp[e)
