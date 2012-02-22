import re
import sys
from cgi import escape

regexes = (
    (re.compile(r'((?:https?://|mailto:)[^ \r\n]+)'),
     r"<a href='\1'>\1</a>"),
    (re.compile(r'^\[([0-9]+)\] (.*)$'),
     r"<span id='{}.\1'>\1</span> \2"),
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

def articles(input):
    post = list()
    header = True
    ref = None

    for line in input:
        if not line: # EOF
            yield

        if header:
            if line == '\n':
                header = False
                post.append('\n<pre>')
            else:
                if ':' not in line:
                    raise ValueError("Not a valid header: {!r}".format(line))

                name, value = line.split(':', 1)
                value = value.rstrip('\n')

                if name == 'time':
                    ref = value
                    post.append("<time datetime='{}' pubdate>{}</time>\n".format(value, value))
                elif name == 'tags':
                    post.append('<span>{}</span>\n'.format(value))
        else:
            if line == '\f\n':
                post.append('</pre>\n')
                yield post
                post = list()
                header = True
                ref = None
            else:
                # FIXME format
                post.append(format(line, ref))

if __name__ == '__main__':
    sys.stdout.write('''<!DOCTYPE html>
<title>Scratch pad</title>
<link rel='stylesheet' href='https://raw.github.com/necolas/normalize.css/master/normalize.css'>
<style>
    body, header, footer { margin: 2em; }
    article > pre { width: 40em; white-space: pre-wrap; }
</style>
<header>This is my strachpad, where I learn and make mistakes.</header>\n''')

    for p in reversed(list(articles(sys.stdin))):
        sys.stdout.write('<article>\n')
        for l in p:
            sys.stdout.write(l)
        sys.stdout.write('</article>\n')

    sys.stdout.write('''\n<hr>
<footer>&copy; 2012 Henry Pr&ecirc;cheur</footer>''')
