import sys
import common

if __name__ == '__main__':
    sys.stdout.write('''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
    <title>Scratch pad</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel='stylesheet'
     href='//cdnjs.cloudflare.com/ajax/libs/normalize/2.1.0/normalize.css'>
    <link rel='stylesheet'
     href='//fonts.googleapis.com/css?family=Source+Code+Pro:400,700|Open+Sans'>
    <style>
        body {
            margin: 0 auto;
            max-width: 50rem;
            font-family: 'Open Sans', sans-serif;
            line-height: 140%;
        }
        p { line-height: 150% }
        code, kbd, pre, samp {
            font-family: 'Source Code Pro', monospace , serif;
        }
        pre {
            background-color: silver;
            border-top: 1px solid grey;
            border-bottom: 1px solid grey;
            padding: 0.5em;
        }
        header, footer { padding: 0.5em; margin: 0.5em }
        article { padding: 1.2em; border-bottom: 1px solid silver }
        a { text-decoration: none; color: #3F72D8; border-bottom: 1px dotted }
        a:hover { border-bottom: 1px solid }

        @media all {html {font-size: 24px;}}
        @media all and (max-width:1000px){html {font-size: 24px;}}
        @media all and (max-width:960px){html {font-size: 23px;}}
        @media all and (max-width:920px){html {font-size: 22px;}}
        @media all and (max-width:880px){html {font-size: 21px;}}
        @media all and (max-width:840px){html {font-size: 20px;}}
        @media all and (max-width:800px){html {font-size: 19px;}}
        @media all and (max-width:760px){html {font-size: 18px;}}
        @media all and (max-width:720px){html {font-size: 17px;}}
        @media all and (max-width:680px){html {font-size: 16px;}}
        @media all and (max-width:640px){html {font-size: 15px;}}
        @media all and (max-width:600px){html {font-size: 14px;}}
        @media all and (max-width:560px){html {font-size: 13px;}}
        @media all and (max-width:520px){html {font-size: 12px;}}
    </style>
</head>
<body class='pure'>
<header>This is my strachpad, where I learn and make mistakes.</header>\n''')

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
