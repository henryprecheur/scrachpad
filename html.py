import sys

class Post(object):
    def __init__(self):
        self._header = True
        self._lines = list()

    def feed(self, line):
        if not line or line == '\f\n':
            self._lines.append('</pre>\n')
            return False

        # Poor's man state management
        if self._header:
            if line == '\n':
                self._header = False
                self._lines.append('\n<pre>')
            else:
                if ':' not in line:
                    raise ValueError("Not a valid header: {!r}".format(line))

                name, value = line.split(':', 1)
                value = value.rstrip('\n')

                if name == 'time':
                    self._lines.append(
                        "<time datetime='{}' pubdate>{}</time>\n".\
                        format(value, value))
                elif name == 'tags':
                    self._lines.append('<p>{}</p>\n'.format(value))
        else:
            self._lines.append(line)

        return True

if __name__ == '__main__':
    posts = list()
    post = Post()

    for line in sys.stdin:
        if not post.feed(line):
            posts.append(post)
            post = Post()

    print len(posts)

    for p in reversed(posts):
        for l in p._lines:
            sys.stdout.write(l)
