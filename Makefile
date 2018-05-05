all:
	scratchpad < log

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

clean:
	rm -f 20[1-9]*.html index.html feed.atom

.PHONY: clean relog all
