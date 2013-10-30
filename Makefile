proof.dvi: proof.tex test.py.tex plots.tex

discovery.tar.gz: Makefile proof.tex test.py plot.py
	$(RM) $@ && tar acf $@ $^ || $(RM) $@

plots.tex: Makefile
	echo 'm(9, x)' | ./plot.py '$$M_{9}(x)$$' > $@ || $(RM) $@

%.py.tex: %.py
	cat -n $< > $<.txt && src2tex $<.txt
	perl -pe 's/\\footline={.*?}//eg;' < $<.txt.tex > $@
	$(RM) $<.txt $<.txt.tex

print: proof.dvi ; dvips $< -o !lpr

clean: ; $(RM) test.py.tex proof.dvi proof.log

.PHONY: clean print
