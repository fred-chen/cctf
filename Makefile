.PHONY: doc

doc:
	mkdir -p doc
	python -m pydoc -w cctf/*.py
	mv -f *.html doc/
