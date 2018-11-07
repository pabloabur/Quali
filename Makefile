# TODO does not work if only a new .eps file is created
thesis = tese
texs = $(wildcard *.tex) \
	   $(wildcard sections/*tex)
bibs = $(wildcard *.bib)
svgs = $(wildcard figuras/*.svg)

all: $(svgs:%.svg=%.eps) $(thesis).pdf
	
figuras/%.eps: figuras/%.svg
	inkscape figuras/$*.svg --export-eps=figuras/$*.eps

$(thesis).pdf: $(thesis).tex $(texs) $(bibs)
	latexmk -pdf $<
	
.PHONY: clean
clean:
	latexmk -C
