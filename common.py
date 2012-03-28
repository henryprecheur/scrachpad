import io

def post(input):
    id_ = input.next().rstrip('\n')

    if input.next() != '\n':
        raise ValueError('Bad ID separator')

    body = io.BytesIO()
    while True:
        line = input.next()

        if line == '\f\n':
            return (id_, body.getvalue())
        else:
            body.write(line)

def posts(input):
    p = list()
    try:
        while True:
            p.append(post(input))
    except StopIteration:
        return p
