import sys
import common

if __name__ == '__main__':
    style = (
        open('normalize.css').read() + open('style.css').read()
    )
    sys.stdout.write('''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
    <title>Scratch pad</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel='stylesheet' type='text/css'
     href='http://fonts.googleapis.com/css?family=Anonymous+Pro'>
    <style>{style}</style>
</head>
<body>
<header>This is my strachpad, where I learn and make mistakes.</header>
'''.format(style=style))

    for id_, body in reversed(common.posts(sys.stdin)):
        sys.stdout.write(
            "<article id='{id}'>\n"
            "<time datetime='{id}' pubdate>"
            "<a href='#{id}'>{id}</a></time>\n".format(id=id_)
        )
        x = common.markdown(body)
        x = x.encode('utf8', 'xmlcharrefreplace')
        sys.stdout.write(x)
        sys.stdout.write('</article>\n')

    sys.stdout.write('''
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
