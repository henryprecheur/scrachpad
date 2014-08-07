import sys

from markdown2 import markdown

import common
from xmlize import xmlize

url = 'http://henry.precheur.org/scratchpad'

if __name__ == '__main__':
    posts = tuple(reversed(common.posts(sys.stdin)))

    updated, _ = posts[0]
    out = sys.stdout.write
    out('''\
<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">

<id>{url}</id>
<title>Scratchpad</title>
<updated>{time}</updated>
<link rel="self" href="{url}/feed.atom" />
<link rel="alternate" type="text/html" href="{url}/" />
'''.format(url=url, time=updated))

    for id_, body in posts:
        # Changed the ID in august 2014
        if id_ < '2014-07':
            entry_id = url + '/#' + id_
        else:
            entry_id = url + '/' + id_

        out('''\
<entry>
  <id>{entry_id}</id>
  <link href='{url}/{ref}' />
  <title>{ref}</title>
  <updated>{ref}</updated>
  <author>
    <name>Henry Pr&#234;cheur</name>
    <email>henry@precheur.org</email>
  </author>
  <content type="xhtml">
    <div xmlns="http://www.w3.org/1999/xhtml">
'''.format(url=url, ref=id_, entry_id=entry_id))
        x = xmlize(markdown(body))
        out(x.encode('utf8', 'xmlcharrefreplace'))
        out('    </div>\n  </content>\n</entry>\n')
out('</feed>')
