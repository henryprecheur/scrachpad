import sys
import common

if __name__ == '__main__':
    sys.stdout.write('''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
    <meta name="viewport" content="width=device-width">
    <title>Scratch pad</title>
    <link rel='stylesheet' href='//cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/2.3.2/css/bootstrap.min.css'>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel='stylesheet' href='//cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/2.3.2/css/bootstrap-responsive.min.css'>
    <style>
        body { margin: 0 auto; max-width: 50em }
        blockquote p { font-size: inherit }
        article > time { display: block; margin-bottom: 1.5em }
    </style>
</head>
<body>
<header>This is my strachpad, where I learn and make mistakes.</header>\n''')

    for id_, body in reversed(common.posts(sys.stdin)):
        sys.stdout.write('<hr>\n'
                         '<article id=%s>\n'
                         "<time datetime=%s pubdate><a href='#%s'>%s</a></time>"
                         '</a>\n' % (id_, id_, id_, id_))
        x = common.markdown(body)
        x = x.encode('utf8', 'xmlcharrefreplace')
        sys.stdout.write(x)
        sys.stdout.write('</article>\n')

    sys.stdout.write('''\n<hr>
<footer>Contact me:
<a href='mailto:Henry Precheur <henry@precheur.org>'>Henry \
Pr&ecirc;cheur</a></footer>

<script type="text/javascript">

  var _gaq = _gaq || [];
  _gaq.push(['_setAccount', 'UA-20945988-4']);
  _gaq.push(['_trackPageview']);

  (function() {
    var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
    ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
  })();

</script>
</body>
</html>
''')
