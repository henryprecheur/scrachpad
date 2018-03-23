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
	var expected = time.Time{}
	if p.Timestamp.Equal(expected) {
		t.Fatalf("bad timestamp: %q != %q", p.Timestamp, expected)
	}
	if _, err = reader.ReadByte(); err != io.EOF {
		t.Fatalf("bad error at the end: %q != %q", err, io.EOF)
	}
}

var exampleLog = ("2011-12-30T21:00:00Z\n\nLet's talk\n\f\n" +
	"2011-12-31T21:00:00Z\n\nLet's talk\n\f\n")

func TestParseLog(t *testing.T) {
	var reader = bufio.NewReader(strings.NewReader(exampleLog))
	var _, err = parseLog(reader)
	if err != io.EOF {
		t.Fatalf("bad error: %q", err)
	}
	/*
		var expected = time.Time{}
		if p.Timestamp.Equal(expected) {
			t.Fatalf("bad timestamp: %q != %q", p.Timestamp, expected)
		}
	*/
	if _, err = reader.ReadByte(); err != io.EOF {
		t.Fatalf("bad error at the end: %q != %q", err, io.EOF)
	}
}
