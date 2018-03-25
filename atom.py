import sys

from markdown2 import markdown

import common
from xmlize import xmlize

if __name__ == '__main__':
    posts = common.posts(sys.stdin)

    updated, _ = posts[0]
    out = sys.stdout.write
    out('''\
<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">

<id>http://henry.precheur.org/scratchpad</id>
<title>Scratchpad</title>
<updated>{time}</updated>
<link rel="self" href="http://henry.precheur.org/scratchpad/feed.atom" />
<link rel="alternate" type="text/html" href="http://henry.precheur.org/scratchpad/" />
'''.format(time=updated))

    for timestamp, body in posts:
        entry_id = common.slug(timestamp)

        out('''\
<entry>
  <id>http://henry.precheur.org/scratchpad/{entry_id}</id>
  <link href='http://henry.precheur.org/scratchpad/{entry_id}' />
  <title>{timestamp}</title>
  <updated>{timestamp}</updated>
  <author>
    <name>Henry Pr&#234;cheur</name>
    <email>henry@precheur.org</email>
  </author>
  <content type="xhtml">
    <div xmlns="http://www.w3.org/1999/xhtml">
'''.format(timestamp=timestamp, entry_id=entry_id))
        x = xmlize(markdown(body))
        out(x.encode('utf8', 'xmlcharrefreplace'))
        out('    </div>\n  </content>\n</entry>\n')
out('</feed>')
