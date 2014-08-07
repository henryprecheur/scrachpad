import sys
import common

def page(title, body):
    style = (
        open('normalize.css').read() + open('style.css').read()
    )

    return ('''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
    <title>{title}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel='stylesheet' type='text/css'
     href='http://fonts.googleapis.com/css?family=Anonymous+Pro'>
    <style>{style}</style>
</head>
<body>
{body}
</body>
<footer>Contact me: <a href='mailto:Henry Precheur <henry@precheur.org>'>
Henry Pr&ecirc;cheur</a></footer>
<script type="text/javascript">

var _gaq = _gaq || [];
_gaq.push(['_setAccount', 'UA-20945988-4']);
_gaq.push(['_trackPageview']);

(function() {{
var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
}})();

</script>

</html>'''
    ).format(title=title, body=body, style=style)

def article(id, body):
    x = common.markdown(body)
    x = x.encode('utf8', 'xmlcharrefreplace')
    return (
        "<article id='{id}'>\n"
        "<time datetime='{id}' pubdate>"
        "<a href='{id}'>{id}</a></time>\n"
        "{body}\n"
        "</article>\n"
    ).format(id=id, body=x)

if __name__ == '__main__':
    articles = list(
        (i, article(i, b))
        for i, b in reversed(common.posts(sys.stdin))
    )

    for id, body in articles:
        open(id + '.html', 'w').write(
            page(
                title='Scratch pad &em; ' + id, body=body
            )
        )

    body = (
        '<header>This is my strachpad, where I learn and make '
        'mistakes.</header>' +
        '\n'.join(i for _, i in articles)
    )

    open('index.html', 'w').write(
        page(
            title='Scratch pad',
            body=body
        )
    )
