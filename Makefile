TEX = $(wildcard *.tex)

all: $(TEX) 
	TEXINPUTS=.//: latexmk -pdf -use-make -outdir=build $(TEX)

.PHONY: clean
clean:
	@rm -f *~
	latexmk -outdir=build -CA
	rm -rf ./build

