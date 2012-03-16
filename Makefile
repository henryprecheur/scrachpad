PYTHON=python

all: index.html feed.atom

index.html: log
	$(PYTHON) html.py < $^ > $@

feed.atom: log
	$(PYTHON) atom.py < $^ > $@

log:
	curl -s http://henry.precheur.org/scratchpad/log > log

clean:
	rm -f index.html feed.atom
