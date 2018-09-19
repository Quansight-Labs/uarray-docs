.PHONY: paper
paper: 
	TEXINPUTS=.//: latexmk -pdf -use-make paper.tex

.PHONY: clean
clean:
	@rm -f *~
	latexmk -CA

