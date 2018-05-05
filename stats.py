from common import posts
from datetime import date

def date_from_id(i):
    i = i[:len('2012-03-28')]
    year, month, day = i.split('-')
    return date(int(year), int(month), int(day))

def sort_by_week(posts):
    weeks = list()

    prev = None
    bodies = list()
    for id_, body in posts:
        d = date_from_id(id_)
        isoweek = '{0:04}-{1:02}'.format(*d.isocalendar())

        if isoweek == prev:
            bodies.append(body)
        else:
            bodies = [body]
            weeks.append((isoweek, bodies))
            prev = isoweek
    return weeks

def stats(texts):
    return (
        sum(len(t) for t in texts),
        sum(len(t.split()) for t in texts)
    )

def html(posts, output):
    output.write('''<!DOCTYPE html>
<title>Scratchpad stats</title>
<ul>
''')
    for week, texts in sort_by_week(posts):
        chars, words = stats(texts)
        output.write('  <li>{week} chars: {chars} words: {words}</li>\n'.\
                     format(chars=chars, words=words, week=week))
    output.write('</table>\n')

def console(posts):
    for week, texts in sort_by_week(p):
        print '{}, {}, {}'.format(week, *stats(texts))

if __name__ == '__main__':
    from sys import stdin, stdout

    p = posts(stdin)

    html(p, stdout)
