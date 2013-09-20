PYTHON=python
VIRTUALENV_URL='https://github.com/pypa/virtualenv/releases/tag/1.10.1'


all: index.html feed.atom

index.html: log html.py
	.env/bin/python html.py < log > $@

feed.atom: log atom.py
	.env/bin/python atom.py < log > $@

bootstrap:
	curl -s $(VIRTUALENV_URL) | tar zxf -
	curl -s $(VIRTUALENV_URL) | $(PYTHON) - .env
	.env/bin/pip install --upgrade html5lib markdown2

log:
	curl -s http://henry.precheur.org/scratchpad/log > log

relog:
	curl -s http://henry.precheur.org/scratchpad/log > log

serve:
	$(PYTHON) -m SimpleHTTPServer 8080

clean:
	rm -f index.html feed.atom normalize.css

.PHONY: clean relog all
