all:
	./scratchpad < log

install: glide
	go install

scratchpad: glide
	go build

glide:
	glide install

log:
	curl -s http://henry.precheur.org/scratchpad/log > log

relog:
	curl -s http://henry.precheur.org/scratchpad/log > log

serve:
	python -m SimpleHTTPServer

clean:
	rm -f 20[1-9]*.html 20[1-9]*/index.html index.html feed.atom
	rmdir 20[1-9]*/

release: scratchpad
	scp scratchpad henry.precheur.org:/var/www/henry.precheur.org/scratchpad

.PHONY: clean relog all
