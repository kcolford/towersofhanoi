all: text2tex proof.dvi archive.tar.gz

archive.tar.gz: Makefile proof.tex test.py text2tex.c
	tar cf $(basename $@) $^ && gzip -f9 $(basename $@)

proof.dvi: proof.tex test.tex plots.tex

echoarg = 'a = [print(m(9, x)) for x in range(300)]'
gnuplotarg = 'set terminal pstex; plot "-" smooth unique title "$$M_9(n)$$"'
plots.tex: test.py
	echo $(echoarg) | python3 -i $< | gnuplot -e $(gnuplotarg) > $@

.py.tex: ; cat -n $< | ./text2tex > $@ || $(RM) $@

print: proof.dvi ; dvips $< -o !lpr

clean:
	$(RM) *~ *.dvi *.log plots.tex test.tex archive.tar.gz text2tex
	$(RM) -r __pycache__

.PHONY: all clean print
.SUFFIXES: .py