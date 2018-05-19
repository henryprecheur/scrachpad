package main

import "text/template"

const (
	base = `{{define "page"}}<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
    <title>{{block "title" .}}Scratch pad{{end}}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" type='text/css' href="{{block "stylePrefix" .}}{{end}}style.css">
</head>
<body>
{{block "body" .}}{{end}}
<footer>
<p>Get the latest updates: <a href='feed.atom'>Atom Feed</a></p>
<p>
Like this blog? Check out my <a href='http://henry.precheur.org'>other blog</a>
for more long-form articles.
</p>
<p>
Looking for a full stack developper in Vancouver BC or remote? I&rsquo;m open
to opportunities, resume available on request. <a
href='mailto:henry@precheur.org'>Feel free to contact me</a>.
</p>
<p>
Have something to say about what you read?<br>
My Email is <a href='mailto:henry@precheur.org'>
Henry Pr&ecirc;cheur &lt;henry@precheur.org&gt;</a>
</p>
</footer>
<style>
@import url('https://fonts.googleapis.com/css?family=Anonymous+Pro');
@font-face {
        font-family: 'Charter';
        src: url('http://henry.precheur.org/scratchpad/charter/regular.eot');
        src: url('http://henry.precheur.org/scratchpad/charter/regular.eot?#iefix') format('embedded-opentype'),
        url('{{template "stylePrefix"}}charter/regular.woff') format('woff');
        font-weight: normal;
        font-style: normal;
        font-display: fallback;
}
@font-face {
        font-family: 'Charter';
        src: url('http://henry.precheur.org/scratchpad/charter/italic.eot');
        src: url('http://henry.precheur.org/scratchpad/charter/italic.eot?#iefix') format('embedded-opentype'),
        url('{{template "stylePrefix"}}charter/italic.woff') format('woff');
        font-weight: normal;
        font-style: italic;
        font-display: fallback;
}
@font-face {
        font-family: 'Charter';
        src: url('http://henry.precheur.org/scratchpad/charter/bold-italic.eot');
        src: url('http://henry.precheur.org/scratchpad/charter/bold-italic.eot?#iefix') format('embedded-opentype'),
        url('{{template "stylePrefix"}}charter/bold-italic.woff') format('woff');
        font-weight: bold;
        font-style: italic;
        font-display: fallback;
}
</style>
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
</html>{{end}}`
	index = `{{define "body"}}<header>Spreading my ignorange</header>{{ range . }}
<article id='{{ .Id }}'>
<time datetime='{{ .Timestamp }}' pubdate><a href='{{ urlquery .Id }}'>{{ .Timestamp }}</a></time>
{{.Body}}
</article>{{end}}{{end}}{{template "page" .}}`
	post = `{{define "body"}}
<article id='{{ .Id }}'>
<div><a href='/scratchpad/'>Index</a></div>
<hr/>
<time datetime='{{ .Timestamp }}' pubdate>{{ .Timestamp }}</time>
{{.Body}}
</article>{{end}}{{define "title"}}{{.Timestamp}}{{end}}{{define "stylePrefix"}}{{end}}{{template "page" .}}`
	atom = `<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
<id>http://henry.precheur.org/scratchpad</id>
<title>Scratchpad</title>
<updated>{{ (index . 0).Timestamp }}</updated>
<link rel="self" href="http://henry.precheur.org/scratchpad/feed.atom" />
<link rel="alternate" type="text/html" href="http://henry.precheur.org/scratchpad/" />{{ range . }}
<entry>
  <id>http://henry.precheur.org/scratchpad/{{ .AtomId }}</id>
  <link href='http://henry.precheur.org/scratchpad/{{ .AtomId }}' />
  <title>{{ .Timestamp }}</title>
  <updated>{{ .Timestamp }}</updated>
  <author>
    <name>Henry Pr&#234;cheur</name>
    <email>henry@precheur.org</email>
  </author>
  <content type="html"><![CDATA[{{ .Body }}]]></content>
</entry>{{end}}
</feed>`
)

var (
	BaseTemplate  = template.Must(template.New("base").Parse(base))
	IndexTemplate = template.Must(
		template.Must(BaseTemplate.Clone()).Parse(index),
	)
	PostTemplate = template.Must(
		template.Must(BaseTemplate.Clone()).Parse(post),
	)
	AtomTemplate = template.Must(template.New("atom").Parse(atom))
)
