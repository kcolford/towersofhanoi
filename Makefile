gen_tex = plots.tex test.tex

all: text2tex proof.dvi archive.tar.gz

archive.tar.gz: Makefile proof.tex test.py plot.py text2tex.c
	tar cf $(basename $@) $^ && gzip -f9 $(basename $@)

proof.dvi: proof.tex test.tex plots.tex

plots.tex: test.py
	echo 'a=[print(m(9,x))for x in range(300)]'|python3 -i $< >plot.dat
	echo 'set term pstex;plot "plot.dat" smooth unique'|gnuplot >$@
	$(RM) plot.dat

.py.tex: ; cat -n $< | ./text2tex > $@ || $(RM) $@

print: proof.dvi ; dvips $< -o !lpr

clean:
	$(RM) *~ *.dvi *.log $(gen_tex) archive.tar.gz text2tex
	$(RM) -r __pycache__

.PHONY: all clean print
.SUFFIXES: .py