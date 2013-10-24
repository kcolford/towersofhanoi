all: proof.dvi

proof.tex: test.py.tex

%.dvi: %.tex; tex $<

%.py.tex: %.py
	link $< temp
	src2tex temp
	perl -pe 's/\\footline={.*?}//eg;' < temp.tex >$@
	unlink temp
	$(RM) temp.tex

%.ps: %.dvi; dvips $<

%.pdf: %.dvi; dvipdf $<

%.html: %.tex; tth < $< > $@

print: proof.ps; lp $^

clean: ; $(RM) test.py.tex proof.dvi proof.log proof.ps proof.pdf

dist:
	$(RM) discovery.tar.gz
	tar zcf discovery.tar.gz Makefile proof.tex test.py

.PHONY: print clean dist
