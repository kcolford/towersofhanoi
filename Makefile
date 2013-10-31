all: proof.dvi
	git archive -o archive.tar.gz HEAD

proof.dvi: proof.tex test.py.tex plots.tex

plots.tex: Makefile
	echo 'm(9, x)' | ./plot.py '$$M_{9}(x)$$' > $@ || $(RM) $@

%.py.tex: %.py
	cat -n $< > $<.txt && src2tex $<.txt
	perl -pe 's/\\footline=?{.*?}//eg;' < $<.txt.tex > $@
	$(RM) $<.txt $<.txt.tex

print: proof.dvi ; dvips $< -o !lpr

clean: ; $(RM) test.py.tex proof.dvi proof.log plots.tex

.PHONY: all clean print
