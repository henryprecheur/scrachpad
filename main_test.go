package main

import (
	"bufio"
	"bytes"
	"fmt"
	"io"
	"strings"
	"testing"
	"time"
)

func TestScanId(t *testing.T) {
	testCases := []struct {
		input     string
		timestamp time.Time
		hasError  bool
	}{
		{
			input:    "",
			hasError: true,
		},
		{
			input:    "foo\n",
			hasError: true,
		},
		{
			input:     "2006-01-02T15:04:05Z\n",
			timestamp: time.Date(2006, time.January, 2, 15, 04, 05, 0, time.UTC),
		},
	}

	for index, tc := range testCases {
		t.Run(fmt.Sprintf("%d", index), func(t *testing.T) {
			var ts, err = scanId(bufio.NewReader(strings.NewReader(tc.input)))
			if tc.hasError != (err != nil) {
				t.Fatalf("bad error: %q", err)
			}
			if ts != tc.timestamp {
				t.Fatalf("bad timestamp %q != %q", ts, tc.timestamp)
			}
		})
	}
}

func TestScanPost(t *testing.T) {
	var reader = bufio.NewReader(strings.NewReader("foo\n\f\nextra"))
	var b, err = scanPost(reader)
	if err != nil {
		t.Fatalf("bad error: %q", err)
	}

	{
		var expected = []byte{'f', 'o', 'o', '\n'}
		if !bytes.Equal(b, expected) {
			t.Fatalf("bad buffer: %q != %q", b, expected)
		}
	}

	{
		var line, err = reader.ReadSlice(0) // read what's left
		if err != io.EOF {
			t.Fatalf("bad error: %q", err)
		}
		var expected = []byte{'e', 'x', 't', 'r', 'a'}
		if !bytes.Equal(line, expected) {
			t.Fatalf("bad left-over data: %q", line)
		}
	}
}

const examplePost = "2011-12-30T21:00:00Z\n\nLet's talk\n\f\n"

func TestParsePost(t *testing.T) {
	var reader = bufio.NewReader(strings.NewReader(examplePost))
	var p, err = parsePost(reader)
	if err != nil {
		t.Fatalf("bad error: %q", err)
	}
	var expected = time.Date(2011, 12, 30, 21, 0, 0, 0, time.UTC)
	if !p.Timestamp.Equal(expected) {
		t.Fatalf("bad timestamp: %q != %q", p.Timestamp, expected)
	}
	if _, err = reader.ReadByte(); err != io.EOF {
		t.Fatalf("bad error at the end: %q != %q", err, io.EOF)
	}
}

func TestParseLog(t *testing.T) {
	var logText = ("2011-12-30T21:00:00Z\n\nLet's talk\n\f\n" +
		"2011-12-31T21:00:00Z\n\nLet's talk\n\f\n")
	var results = []Post{
		{
			Timestamp: time.Date(2011, 12, 30, 21, 00, 00, 0, time.UTC),
			Body:      []byte("Let's talk\n"),
		},
		{
			Timestamp: time.Date(2011, 12, 31, 21, 00, 00, 0, time.UTC),
			Body:      []byte("Let's talk\n"),
		},
	}

	var reader = bufio.NewReader(strings.NewReader(logText))
	var log, err = parseLog(reader)
	if err != io.EOF {
		t.Fatalf("bad error: %q", err)
	}

	for index, expected := range results {
		var p = log[index]

		if p.Timestamp != expected.Timestamp {
			t.Fatalf("%q != %q", p.Timestamp, expected.Timestamp)
		}

		if !bytes.Equal(p.Body, expected.Body) {
			t.Fatalf("%q != %q", p.Body, expected.Body)
		}
	}

	if _, err = reader.ReadByte(); err != io.EOF {
		t.Fatalf("bad error at the end: %q != %q", err, io.EOF)
	}
}
