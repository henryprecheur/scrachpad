import io

from dateutil.parser import parse
from markdown2 import markdown

def posts_iter(input):
    for line in input:
        timestamp = line.rstrip()

        if input.next() != '\n':
            raise ValueError('Bad ID separator')

        body = io.BytesIO()
        while True:
            line = input.next()

            if line == '\f\n':
                yield (
                    timestamp,
                    markdown(
                        body.getvalue(),
                        extras=('code-friendly', 'smarty-pants'),
                    )
                )
                break
            else:
                body.write(line)

def posts(input):
    return tuple(reversed(tuple(posts_iter(input))))

def slug(timestamp):
    if timestamp < '2018-04':
        return timestamp
    else:
        return parse(timestamp).strftime('%Y%m%d_%H%M%S')
