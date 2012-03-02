import re
from cgi import escape

regexes = (
    (re.compile(r'((?:https?://|mailto:)[^ \r\n]+)'),
     r"<a href='\1'>\1</a>"),
    (re.compile(r'^\[([0-9]+)\] (.*)$'),
     r"<span id='%s.\1'>\1 &mdash; \2</span>"),
    (re.compile(r'\[([0-9]+)\]'),
     r"<sup><a href='#%s.\1'>\1</a></sup>"),
    (re.compile(r'\[\[([0-9]+)\]\]'), r'[\1]')
)

def format(line, ref):
    assert ref

    line = escape(line)
    for r, s in regexes:
        try:
            s = s % ref
        except TypeError:
            pass
        line = r.sub(s, line)
    return line

def post(input):
    id_ = input.next().rstrip('\n')

    if input.next() != '\n':
        raise ValueError('Bad ID separator')

    body = list()
    while True:
        line = input.next()

        if line == '\f\n':
            return (id_, body)
        else:
            body.append(line)

def posts(input):
    p = list()
    try:
        while True:
            p.append(post(input))
    except StopIteration:
        return p
