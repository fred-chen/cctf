.PHONY: doc

doc:
	mkdir -p doc
	pdoc3 --force --html -o doc cctf
	mv -f doc/cctf/*.html doc/ && rmdir doc/cctf
