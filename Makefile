proof.dvi: proof.tex test.tex

%.dvi: %.tex; tex $<

%.tex: %.py
	$tmpfile=`mktemp`
	cat $< > $tmpfile
	src2tex $tmpfile
	perl -pe 's/\\footline={.*?}//eg;' < $tmpfile.tex > $@
	$(RM) $tmpfile $tmpfile.tex

%.ps: %.dvi; dvips $<

%.pdf: %.dvi; dvipdf $<

pdf: proof.pdf

print: proof.ps; lp $^

clean: ; $(RM) test.tex proof.dvi proof.log proof.ps

dist:
	$(RM) discovery.tar.gz
	tar zcf discovery.tar.gz Makefile proof.tex test.py

.PHONY: pdf print clean dist
