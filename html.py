import sys
import common
from urllib import quote

def page(title, body):
    return ('''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
    <title>{title}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel='stylesheet' type='text/css' href='http://fonts.googleapis.com/css?family=Anonymous+Pro'>
    <link rel="stylesheet" type='text/css' href="style.css">
</head>
<body>
{body}
</body>
<footer>
<p>
Like this blog? Check out my <a href='http://henry.precheur.org'>other blog</a>
for more long-form articles.
</p>
<p>
Looking for a backend developper in Vancouver BC or remote? I&rsquo;m open to
opportunities. <a href='mailto:Henry Precheur <henry@precheur.org>'>Feel free
to contact me</a>.
</p>
<p>
Have something to say about what you read?<br>
My Email is <a href='mailto:Henry Precheur <henry@precheur.org>'>
Henry Pr&ecirc;cheur &lt;henry@precheur.org&gt;</a>
</p>
</footer>

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
    ).format(title=title, body=body)

def index_article(timestamp, body):
    slug = common.slug(timestamp)
    return (
        "<article id='{slug}'>\n"
        "<time datetime='{timestamp}' pubdate>"
        "<a href='{href}'>{timestamp}</a></time>\n"
        "{body}\n"
        "</article>\n"
    ).format(href=quote(slug),
             slug=slug,
             timestamp=timestamp,
             body=body)

def page_article(timestamp, body):
    return (
        "<article id='{slug}'>\n"
        "<div><a href='/scratchpad'>Index</a></div>\n<hr/>\n"
        "<time datetime='{timestamp}' pubdate>{timestamp}</time>\n"
        "{body}\n"
        "</article>\n"
    ).format(slug=common.slug(timestamp),
             timestamp=timestamp,
             body=body)

if __name__ == '__main__':
    posts = list(
        (timestamp, body.encode('utf8', 'xmlcharrefreplace'))
        for timestamp, body in common.posts(sys.stdin)
    )

    for timestamp, body in posts:
        open(common.slug(timestamp) + '.html', 'w').write(
            page(title=timestamp, body=page_article(timestamp, body))
        )

    body = (
        '<header>Spreading my ignorange</header>' +
        '\n'.join(index_article(t, b) for t, b in posts)
    )

    open('index.html', 'w').write(
        page(
            title='Scratch pad',
            body=body
        )
    )
