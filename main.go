package main

import (
	"bufio"
	"bytes"
	"fmt"
	"io"
	"log"
	"os"
	"path"
	"time"

	blackfriday "gopkg.in/russross/blackfriday.v2"
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
			Body:      string(blackfriday.Run(p.Body)),
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

func openFile(filename string) (*os.File, error) {
	return os.OpenFile(filename, os.O_WRONLY|os.O_CREATE|os.O_TRUNC, 0666)
}

func makeAtom(posts []HTMLPost) error {
	output, err := openFile("feed.atom")
	defer output.Close()
	if err != nil {
		return err
	}

	return AtomTemplate.Execute(output, posts)
}

func makeIndexHTML(posts []HTMLPost) error {
	output, err := openFile("index.html")
	if err != nil {
		return err
	}
	defer output.Close()

	return IndexTemplate.Execute(output, posts)
}

func makePagesHTML(posts []HTMLPost) error {
	for _, post := range posts {
		// use subdir to store post
		if err := os.Mkdir(post.Id, 0777); err != nil && !os.IsExist(err) {
			return err
		}

		var file, err = openFile(path.Join(post.Id, "index.html"))
		if err != nil {
			return err
		}

		err = PostTemplate.Execute(file, post)
		if err1 := file.Close(); err == nil {
			err = err1
		}
		if err != nil {
			return err
		}
	}
	return nil
}

func makeHTML(posts []HTMLPost) error {
	if err := makeIndexHTML(posts); err != nil {
		return err
	}

	return makePagesHTML(posts)
}

func main() {

	posts, err := parseLog(bufio.NewReader(os.Stdin))
	if err != io.EOF {
		log.Fatalf("error while parsing: %s", err)
	}

	var h = processPosts(posts)

	if err := makeAtom(h); err != nil {
		log.Fatal(err)
	}

	if err := makeHTML(h); err != nil {
		log.Fatal(err)
	}
}
