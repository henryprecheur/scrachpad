import sys
from string import Template

import common

url = 'http://henry.precheur.org/scratchpad'

if __name__ == '__main__':
    posts = tuple(reversed(common.posts(sys.stdin)))

    updated, _ = posts[0]
    sys.stdout.write(Template('''\
<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">

<id>${url}</id>
<title>Scratchpad</title>
<updated>${time}</updated>
<link rel="self" href="$url/feed.atom" />
<link rel="self" href="$url/" />\n
''').safe_substitute(url=url, time=updated))

    for id_, body in posts:
        sys.stdout.write(Template('''\
<entry>
  <id>${url}/#${ref}</id>
  <link href='${url}/#${ref}' />
  <title>${ref}</title>
  <updated>${ref}</updated>
  <content type="xhtml">
    <div xmlns="http://www.w3.org/1999/xhtml"><pre>''').\
                         safe_substitute(url=url, ref=id_))
        for l in body:
            sys.stdout.write(common.format(l, id_))
        sys.stdout.write('    </pre></div>\n  </content>\n</entry>\n')

    sys.stdout.write('</feed>')
