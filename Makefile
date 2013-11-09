distfiles = README LICENSE Makefile proof.tex test.py
subdirs = ascii2tex

all: proof.dvi archive.tar.gz

$(addsuffix /%, $(subdirs)):
	$(MAKE) -C $(dir $@) $(notdir $@)

archive.tar.gz: $(distfiles) $(addsuffix /archive.tar.gz, $(subdirs))
	tar cf $(basename $@) $^ && gzip -f9 $(basename $@)

proof.dvi: proof.tex test.tex plots.tex

echoarg = 'a = [print(m(9, x)) for x in range(300)]'
gnuplotarg = 'set terminal pstex; plot "-" smooth unique title "$$M_9(n)$$"'
plots.tex: test.py
	echo $(echoarg) | python3 -i $< | gnuplot -e $(gnuplotarg) > $@

.py.tex:
	$(MAKE) ascii2tex/ascii2tex
	cat -n $< | ./ascii2tex/ascii2tex > $@

print: proof.dvi
	dvips $< -o !lpr

clean: $(addsuffix /clean, $(subdirs))
	$(RM) *.dvi *.log plots.tex test.tex archive.tar.gz

.PHONY: all clean print
.SUFFIXES: .py
