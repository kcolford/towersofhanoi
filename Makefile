all: proof.dvi archive.tar.gz

Makefile: ascii2tex
	$(MAKE) -C $?

archive.tar.gz: README LICENSE Makefile proof.tex test.py
	tar cf $(basename $@) $^ ascii2tex/$@
	gzip -f9 $(basename $@)

proof.dvi: proof.tex test.tex plots.tex

echoarg = 'a = [print(m(9, x)) for x in range(300)]'
gnuplotarg = 'set terminal pstex; plot "-" smooth unique title "$$M_9(n)$$"'
plots.tex: test.py
	echo $(echoarg) | python3 -i $< | gnuplot -e $(gnuplotarg) > $@

.py.tex:
	$(MAKE) -C ascii2tex
	cat -n $< | ./ascii2tex/ascii2tex > $@

print: proof.dvi
	dvips $< -o !lpr

clean:
	$(RM) *.dvi *.log plots.tex test.tex

.PHONY: all clean print
.SUFFIXES: .py
