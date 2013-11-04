all: text2tex proof.dvi archive.tar.gz

archive.tar.gz: Makefile proof.tex test.py plot.py text2tex.c
	$(RM) $@; tar acf $@ $^

proof.dvi: proof.tex test.tex plots.tex

plots.tex:
	echo 'm(9, x)' | ./plot.py '$$M_{9}(x)$$' > $@ || $(RM) $@

.py.tex: ; cat -n $< | ./text2tex > $@ || $(RM) $@

print: proof.dvi ; dvips $< -o !lpr

clean:
	$(RM) *~ *.dvi *.log plots.tex test.tex archive.tar.gz text2tex
	$(RM) -r __pycache__

.PHONY: all clean print
.SUFFIXES: .py