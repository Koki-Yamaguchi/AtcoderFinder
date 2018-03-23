.PHONY: open build

open: index.html
	open index.html

build: index.html

index.html: generator.py
	python3 $< > $@
