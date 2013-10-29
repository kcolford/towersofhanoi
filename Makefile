proof.dvi: proof.tex test.py.tex

discovery.tar.gz: Makefile proof.tex test.py
	$(RM) $@ && tar acf $@ $^

%.py.tex: %.py
	cat -n $< > $<.txt && src2tex $<.txt
	perl -pe 's/\\footline={.*?}//eg;' < $<.txt.tex > $@
	$(RM) $<.txt $<.txt.tex

%.ps: %.dvi ; dvips $<

print: proof.ps; lp $^

clean: ; $(RM) test.py.tex proof.dvi proof.log proof.ps discovery.tar.gz

.PHONY: clean print
