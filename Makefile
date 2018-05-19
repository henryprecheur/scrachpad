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

serve: all
	# create links to deps
	for i in 20[1-9]*/; do \
		test -e $$i/style.css || cp ./style.css $$i/; \
		test -e $$i/charter || cp -r ./charter $$i/; \
	done
	python -m SimpleHTTPServer

clean:
	-rm -rf 20[1-9]*.html index.html feed.atom 20[1-9]*/

release: scratchpad
	scp -C scratchpad henry.precheur.org:/var/www/henry.precheur.org/scratchpad

.PHONY: clean relog all
