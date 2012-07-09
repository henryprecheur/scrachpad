import io
import xml.etree
import html5lib

def xmlize(input_, encoding=None, output=None):
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
    encoding = encoding or 'utf_8'
    doc = html5lib.parseFragment(input_,
                                 encoding=encoding,
                                 treebuilder='etree',
                                 namespaceHTMLElements=False)

    walker = html5lib.treewalkers.getTreeWalker('etree', xml.etree.ElementTree)
    s = html5lib.serializer.XHTMLSerializer()

    stream = s.serialize(walker(doc), encoding='utf-8')
    if output:
        for text in stream:
            output.write(text)
    else:
        return u''.join(unicode(x, encoding) for x in stream)
    stdout.write(xmlize(stdin))
