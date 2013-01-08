PYTHON=.env/bin/python

all: index.html style.css feed.atom

index.html: log html.py
	$(PYTHON) html.py < log > $@

feed.atom: log atom.py
	$(PYTHON) atom.py < log > $@

style.css: normalize.css extra.css
	cat normalize.css extra.css > style.css

normalize.css:
	curl -s https://raw.github.com/necolas/normalize.css/master/normalize.css > $@

log:
	curl -s http://henry.precheur.org/scratchpad/log > log

relog:
	curl -s http://henry.precheur.org/scratchpad/log > log

clean:
	rm -f index.html feed.atom normalize.css

.PHONY: clean relog all
