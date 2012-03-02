import sys
import common

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

    for id_, body in reversed(common.posts(sys.stdin)):
        sys.stdout.write('<article>\n<time datetime=%s pubdate>%s</time>\n'
                         '<pre>' % (id_, id_))
        for l in body:
            sys.stdout.write(common.format(l, id_))
        sys.stdout.write('</pre>\n</article>\n')

    sys.stdout.write('''\n<hr>
<footer>&copy; 2012 \
<a href='mailto:Henry Precheur <henry@precheur.org>'>Henry \
Pr&ecirc;cheur</a></footer>''')
