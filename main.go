package main

import (
	"bufio"
	"bytes"
	"fmt"
	"io"
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

func main() {
	var reader = bufio.NewReader(os.Stdin)

	parseLog(reader)
}
