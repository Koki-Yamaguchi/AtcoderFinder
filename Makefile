.PHONY: all
all: index.html about.html specific.html

index.html: index.py footer.py header.py table.py ACfilter.py form.py main.py classifier.py
	python3 $< > $@
about.html: about.py footer.py header.py table.py ACfilter.py form.py main.py classifier.py
	python3 $< > $@
specific.html: specific.py footer.py header.py table.py ACfilter.py form.py main.py classifier.py
	python3 $< > $@
