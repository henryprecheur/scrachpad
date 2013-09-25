VIRTUALENV=virtualenv

all: index.html feed.atom

index.html: log html.py style.css
	.env/bin/python html.py < log > $@

feed.atom: log atom.py
	.env/bin/python atom.py < log > $@

bootstrap:
	$(VIRTUALENV) .env
	.env/bin/pip install --upgrade html5lib markdown2

log:
	curl -s http://henry.precheur.org/scratchpad/log > log

relog:
	curl -s http://henry.precheur.org/scratchpad/log > log

serve:
	.env/bin/python -m SimpleHTTPServer

clean:
	rm -f index.html feed.atom normalize.css

.PHONY: clean relog all
