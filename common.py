import io
from markdown2 import markdown as _markdown

def posts_iter(input):
    for line in input:
        id_ = line.rstrip('\n')

        if input.next() != '\n':
            raise ValueError('Bad ID separator')

        body = io.BytesIO()
        while True:
            line = input.next()

            if line == '\f\n':
                yield (id_, body.getvalue())
                break
            else:
                body.write(line)

def posts(input):
    return list(posts_iter(input))

def markdown(string):
    return _markdown(
        string,
        extras=('code-friendly', 'smarty-pants')
    )
