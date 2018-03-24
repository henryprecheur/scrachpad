package main

import (
	"bufio"
	"bytes"
	"fmt"
	"io"
	"log"
	"os"
	"time"

	_ "github.com/russross/blackfriday"
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
const pageTemplate = `<!DOCTYPE html>
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
{{ .Body }}
</body>
<footer>Contact me: <a href='mailto:Henry Precheur <henry@precheur.org>'>Henry Pr&ecirc;cheur</a></footer>
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
</html>`

const atomTemplate = `<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">

<id>{{ .Url }}</id>
<title>Scratchpad</title>
<updated>{{ .Updated }}</updated>
<link rel="self" href="{{ .Url }}/feed.atom" />
<link rel="alternate" type="text/html" href="{{ .Url }}/" />
{{ range .Posts }}
{{ end }}
'''.format(url=url, time=updated))

    for id_, body in posts:
        # Changed the ID in august 2014
        if id_ < '2014-07':
            entry_id = url + '/#' + id_
        else:
            entry_id = url + '/' + id_

        out('''\
<entry>
  <id>{entry_id}</id>
  <link href='{url}/{ref}' />
  <title>{ref}</title>
  <updated>{ref}</updated>
  <author>
    <name>Henry Pr&#234;cheur</name>
    <email>henry@precheur.org</email>
  </author>
  <content type="xhtml">
    <div xmlns="http://www.w3.org/1999/xhtml">
'''.format(url=url, ref=id_, entry_id=entry_id))
        x = xmlize(markdown(body))
        out(x.encode('utf8', 'xmlcharrefreplace'))
        out('    </div>\n  </content>\n</entry>\n')
out('</feed>')
`

func makeAtom(posts []Post, writer io.Writer) error {

}

func main() {
	var posts, err = parseLog(bufio.NewReader(os.Stdin))
	if err != io.EOF {
		log.Fatalf("error while parsing: %s", err)
	}
	fmt.Printf("%q\n", posts)
}
