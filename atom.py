import io
import sys

from urllib import quote
from dateutil.parser import parse
import xml.etree
import html5lib

import common

def xmlize(input_, output=None):
    '''
    Convert HTML into XHTML.

    `input_` is a string or a file-like object with a read() method. `output`
    should be a file-like object with a write() method.

    If `output` is passed, `xmlize` write the result into it. Otherwise it
    returns the result as a string::

        >>> xmlize('<p>Hello<br>World')
        u'<p>Hello<br />World</p>'

    If your manipulating files or sockets, you can use the file-like
    interface::

        >>> import io
        >>> input = io.BytesIO('<p>Hello<br>World')
        >>> xmlize(input)
        u'<p>Hello<br />World</p>'
    '''
    assert isinstance(input_, unicode)
    doc = html5lib.parseFragment(input_,
                                 treebuilder='etree',
                                 namespaceHTMLElements=False)

    walker = html5lib.treewalkers.getTreeWalker('etree', xml.etree.ElementTree)
    s = html5lib.serializer.HTMLSerializer(
        omit_optional_tags=False,
        minimize_boolean_attributes=False,
        use_trailing_solidus=True,
        quote_attr_values='always')

    stream = s.serialize(walker(doc), encoding='utf-8')
    if output:
        for text in stream:
            output.write(text)
    else:
        return u''.join(unicode(x, 'utf8') for x in stream)
    stdout.write(xmlize(stdin))

def atom_id(timestamp):
    if timestamp < '2014-07':
        return '#' + timestamp
    elif timestamp < '2018-04':
        return timestamp
    else:
        return parse(timestamp).strftime('%Y%m%d_%H%M%S')


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
        entry_id = atom_id(timestamp)
        slug = quote(common.slug(timestamp))

        out('''\
<entry>
  <id>http://henry.precheur.org/scratchpad/{entry_id}</id>
  <link href='http://henry.precheur.org/scratchpad/{slug}' />
  <title>{timestamp}</title>
  <updated>{timestamp}</updated>
  <author>
    <name>Henry Pr&#234;cheur</name>
    <email>henry@precheur.org</email>
  </author>
  <content type="xhtml">
    <div xmlns="http://www.w3.org/1999/xhtml">
'''.format(timestamp=timestamp, entry_id=entry_id, slug=slug))
        x = xmlize(body)
        out(x.encode('utf8', 'xmlcharrefreplace'))
        out('    </div>\n  </content>\n</entry>\n')
    out('</feed>')
