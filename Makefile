VIRTUALENV=virtualenv

all: index.html feed.atom

index.html: log html.py common.py
	.env/bin/python html.py < log > $@

feed.atom: log atom.py xmlize.py common.py
	.env/bin/python atom.py < log > $@

bootstrap:
	$(VIRTUALENV) .env
	.env/bin/pip install -r requirements.txt

log:
	curl -s http://henry.precheur.org/scratchpad/log > log

relog:
	curl -s http://henry.precheur.org/scratchpad/log > log

clean:
	rm -f 20[1-9]*.html index.html feed.atom

.PHONY: clean relog all
