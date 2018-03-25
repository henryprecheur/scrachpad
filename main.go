package main

import (
	"bufio"
	"bytes"
	"fmt"
	"io"
	"io/ioutil"
	"log"
	"os"
	"text/template"
	"time"

	"github.com/russross/blackfriday"
)

type Post struct {
	Timestamp time.Time
	Body      []byte
}

func scanId(reader *bufio.Reader) (time.Time, error) {
	var buf bytes.Buffer

	for {
		var c, _, err = reader.ReadRune()
		if err != nil {
			return time.Time{}, err
		}
		if c == '\n' {
			break
		}
		buf.WriteRune(c)
	}

	return time.Parse(time.RFC3339, buf.String())
}

func scanHeaderSep(reader *bufio.Reader) error {
	var c, _, err = reader.ReadRune()
	if err != nil {
		return err
	} else if c != '\n' {
		return fmt.Errorf("got: %c expected empty line", c)
	}
	return nil
}

func scanPost(reader *bufio.Reader) ([]byte, error) {
	var buf bytes.Buffer

	for {
		var c, _, err = reader.ReadRune()
		if err != nil {
			return buf.Bytes(), err
		}
		if c == '\f' {
			// check if we've reached the end of the post
			var n, _, _ = reader.ReadRune()
			if n == '\n' {
				break
			} else {
				reader.UnreadRune()
			}
		}
		buf.WriteRune(c)
	}

	return buf.Bytes(), nil
}

func parsePost(reader *bufio.Reader) (Post, error) {
	var p Post
	var err error

	if p.Timestamp, err = scanId(reader); err != nil {
		return p, err
	}

	if err = scanHeaderSep(reader); err != nil {
		return p, err
	}

	if p.Body, err = scanPost(reader); err != nil {
		return p, err
	}

	return p, err
}

func parseLog(reader io.Reader) ([]Post, error) {
	var r = bufio.NewReader(reader)

	var posts []Post
	for {
		var post, err = parsePost(r)
		if err != nil {
			return posts, err
		}
		posts = append(posts, post)
	}

	return posts, nil
}

//
// HTML generation
//
type HTMLPost struct {
	Id        string
	AtomId    string
	Timestamp string
	Body      string
}

//
// 1. generate id from timestamp
// 2. format timestamp
// 3. process body with blackfriday markdown processor
//
func processPosts(posts []Post) []HTMLPost {
	var r []HTMLPost

	for _, p := range posts {
		var id, atomId string

		ts := p.Timestamp
		// keep old IDs intact so they don't get reposted
		if ts.Before(time.Date(2018, 3, 24, 0, 0, 0, 0, time.UTC)) {
			id = ts.Format(time.RFC3339)
			if ts.Before(time.Date(2014, 7, 1, 0, 0, 0, 0, time.UTC)) {
				atomId = "#" + id
			} else {
				atomId = id
			}
		} else {
			id = ts.Format("20060102_150405")
			atomId = id
		}

		var h = HTMLPost{
			Id:        id,
			AtomId:    atomId,
			Timestamp: p.Timestamp.Format(time.RFC3339),
			Body:      string(blackfriday.MarkdownCommon(p.Body)),
		}
		r = append(r, h)
	}

	var res []HTMLPost
	// reverse order
	for i := len(r); i > 0; i-- {
		res = append(res, r[i-1])
	}
	return res
}

const atomTemplate = `<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">

<id>http://henry.precheur.org/scratchpad</id>
<title>Scratchpad</title>
<updated>{{ .Updated }}</updated>
<link rel="self" href="http://henry.precheur.org/scratchpad/feed.atom" />
<link rel="alternate" type="text/html" href="http://henry.precheur.org/scratchpad/" />{{ range .Posts }}
<entry>
  <id>http://henry.precheur.org/scratchpad/{{ .AtomId }}</id>
  <link href='http://henry.precheur.org/scratchpad/{{ .AtomId }}' />
  <title>{{ .Timestamp }}</title>
  <updated>{{ .Timestamp }}</updated>
  <author>
    <name>Henry Pr&#234;cheur</name>
    <email>henry@precheur.org</email>
  </author>
  <content type="xhtml">
    <div xmlns="http://www.w3.org/1999/xhtml">
{{ .Body }}</div>
  </content>
</entry>{{ end }}
</feed>`

func makeAtom(posts []HTMLPost, writer io.Writer) error {
	tmpl, err := template.New("atom").Parse(atomTemplate)
	if err != nil {
		return err
	}

	var x = struct {
		Updated string
		Posts   []HTMLPost
	}{
		Updated: posts[0].Timestamp,
		Posts:   posts,
	}
	err = tmpl.Execute(writer, x)
	if err != nil {
		return err
	}

	return nil
}

const htmlPageTemplate = `{{ define "article" }}
<article id='{{ .Timestamp }}'>
<time datetime='{{ .Timestamp }}' pubdate><a href='{{ urlquery .Id }}'>{{ .Timestamp }}</a></time>
{{ .Body }}
</article>
{{ end }}<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
    <title>{{ .Title }}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel='stylesheet' type='text/css' href='http://fonts.googleapis.com/css?family=Anonymous+Pro'>
    <style>{{ .Style }}</style>
</head>
<body>
{{ block "body" . }}{{ template "article" .Post }}{{ end }}
</body>
<footer>Contact me: <a href='mailto:Henry Precheur <henry@precheur.org>'>Henry Pr&ecirc;cheur</a></footer>
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
</html>`

const htmlIndexTemplate = `{{ define "body" }}<header>Spreading my ignorange</header>
{{ range .Posts }}{{ template "article" . }}{{ end }}{{ end }}`

func readStyle() (string, error) {
	norm, err := ioutil.ReadFile("normalize.css")
	if err != nil {
		return "", err
	}
	style, err := ioutil.ReadFile("style.css")
	if err != nil {
		return "", err
	}
	var buf bytes.Buffer
	buf.Write(norm)
	buf.Write(style)
	return buf.String(), nil
}

func openFile(filename string) (*File, error) {

}

func makeIndexHTML(base *template.Template, posts []HTMLPost, style string) error {
	indexTmpl, err := template.Must(base.Clone()).Parse(htmlIndexTemplate)
	if err != nil {
		return err
	}

	indexFile, err := os.OpenFile("index.html", os.O_WRONLY|os.O_CREATE|os.O_TRUNC, 0)
	if err != nil {
		return err
	}

	var x = struct {
		Title string
		Style string
		Posts []HTMLPost
	}{
		Title: "Scratch pad",
		Style: style,
		Posts: posts,
	}

	err = indexTmpl.Execute(indexFile, x)
	if err1 := indexFile.Close(); err == nil {
		err = err1
	}
	return err
}

func makePagesHTML(tmpl *template.Template, posts []HTMLPost, style string) error {

}

func makeHTML(posts []HTMLPost) error {
	tmpl, err := template.New("page.html").Parse(htmlPageTemplate)
	if err != nil {
		return err
	}

	style, err := readStyle()
	if err != nil {
		return err
	}

	return makeIndexHTML(tmpl, posts, style)
}

func main() {
	var posts, err = parseLog(bufio.NewReader(os.Stdin))
	if err != io.EOF {
		log.Fatalf("error while parsing: %s", err)
	}

	var h = processPosts(posts)

	atomFile, err := os.OpenFile("feed.atom", os.O_WRONLY|os.O_CREATE|os.O_TRUNC, 0)
	makeAtom(h, atomFile)
	atomFile.Close()

	fmt.Println(makeHTML(h))
}
