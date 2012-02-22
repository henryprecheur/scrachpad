import sys

class Post(dict):
    def __init__(self):
        self._header = True
        self._body = list()

    def feed(self, line):
        if not line or line == '\f\n':
            return False

        # Poor's man state management
        if self._header:
            if line == '\n':
                self._header = False
            else:
                if ':' not in line:
                    raise ValueError("Not a valid header: {!r}".format(line))

                name, value = line.split(':', 1)
                self[name] = value.rstrip('\n')
        else:
            self._body.append(line)

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
        print p['tags'], p['time']
        for l in p._body:
            sys.stdout.write(l)
