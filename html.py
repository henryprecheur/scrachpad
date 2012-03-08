import sys
import common

if __name__ == '__main__':
    sys.stdout.write('''<!DOCTYPE html>
<title>Scratch pad</title>
<style>
    html { font: normal medium sans-serif; }
    body { margin: 0 0 0 10%; }
    header, footer, article { margin: 1em; }
    article > p { font: normal 1em monospace; width: 48em }
</style>
<header>This is my strachpad, where I learn and make mistakes.</header>\n''')

    for id_, body in reversed(common.posts(sys.stdin)):
        sys.stdout.write('<article id=%s>\n'
                         '<a href=#%s>'
                         '<time datetime=%s pubdate>%s</time>'
                         '</a>\n'
                         '<p><code>' % (id_, id_, id_, id_))
        for l in body:
            sys.stdout.write(common.format(l, id_))
        sys.stdout.write('</code></p>\n</article>\n')

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

</script>''')
