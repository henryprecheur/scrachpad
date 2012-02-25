import re
import sys
from cgi import escape

regexes = (
    (re.compile(r'((?:https?://|mailto:)[^ \r\n]+)'),
     r"<a href='\1'>\1</a>"),
    (re.compile(r'^\[([0-9]+)\] (.*)$'),
     r"<span id='{}.\1'>\1 &mdash; \2</span>"),
    (re.compile(r'\[([0-9]+)\]'),
     r"<sup><a href='#{}.\1'>\1</a></sup>"),
    (re.compile(r'\[\[([0-9]+)\]\]'), r'[\1]')
)

def format(line, ref):
    assert ref

    line = escape(line)
    for r, s in regexes:
        line = r.sub(s.format(ref), line)
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

if __name__ == '__main__':
    sys.stdout.write('''<!DOCTYPE html>
<title>Scratch pad</title>
<link rel='stylesheet' href='https://raw.github.com/necolas/normalize.css/master/normalize.css'>
<style>
    html { font-family: sans-serif; }
    body, header, footer, article { margin: 2em; }
    article > pre { width: 48em; white-space: pre-wrap; }
</style>
<header>This is my strachpad, where I learn and make mistakes.</header>\n''')

    for id_, body in reversed(posts(sys.stdin)):
        sys.stdout.write('<article>\n<time datetime={} pubdate>{}</time>\n'
                         '<pre>'.format(id_, id_))
        for l in body:
            sys.stdout.write(format(l, id_))
        sys.stdout.write('</pre>\n</article>\n')

    sys.stdout.write('''\n<hr>
<footer>&copy; 2012 \
<a href='mailto:Henry Precheur <henry@precheur.org>'>Henry \
Pr&ecirc;cheur</a></footer>''')
