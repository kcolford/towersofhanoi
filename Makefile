all: proof.dvi

proof.tex: test.py.tex

%.py.tex: %.py
	cat -n $< > $<.txt
	src2tex $<.txt
	perl -pe 's/\\footline={.*?}//eg;' < $<.txt.tex > $@
	$(RM) $<.txt $<.txt.tex

%.ps: %.dvi ; dvips $<

%.pdf: %.dvi ; dvipdf $<

print: proof.ps; lp $^

clean: ; $(RM) test.py.tex proof.dvi proof.log proof.ps proof.pdf

dist:
	$(RM) discovery.tar.gz
	tar zcf discovery.tar.gz Makefile proof.tex test.py

.PHONY: print clean dist
