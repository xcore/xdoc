# default target
LATEX_CMD = latex

lc = $(subst A,a,$(subst B,b,$(subst C,c,$(subst D,d,$(subst E,e,$(subst F,f,$(subst G,g,$(subst H,h,$(subst I,i,$(subst J,j,$(subst K,k,$(subst L,l,$(subst M,m,$(subst N,n,$(subst O,o,$(subst P,p,$(subst Q,q,$(subst R,r,$(subst S,s,$(subst T,t,$(subst U,u,$(subst V,v,$(subst W,w,$(subst X,x,$(subst Y,y,$(subst Z,z,$1))))))))))))))))))))))))))

space :=
space +=


DO_LATEX = echo Running LaTeX;export TEXINPUTS=$(T):_build/xlatex:;pdflatex -interaction nonstopmode $1 > _build/xlatex/latex.log.0;pdflatex -interaction nonstopmode $1 > _build/xlatex/latex.log.1; mv *.aux _build/xlatex; mv *.log _build/xlatex;mv *.idx _build/xlatex; mv *.out _build/xlatex;mv $1 _build/xlatex


OTHER_DOC_DIRS_ABS = $(foreach x,$(OTHER_DOC_DIRS),$(abspath $x))
ifeq ($(OTHER_DOC_DIRS),)
LINKED_DIRS =
else
_link_dir:
	-mkdir _linked_dirs

%.link: | _link_dir
	-ln -T -s $(abspath $*) _linked_dirs/$(notdir $(abspath $*))

_linked_dirs: $(foreach x, $(OTHER_DOC_DIRS), $(x).link)
	@echo "Created linked dirs"
LINKED_DIRS = _linked_dirs
endif

export LINKED_DIRS
export OTHER_DOC_DIRS
export OTHER_DOC_DIRS_ABS

export DO_LATEX

XDOC_MAKEFILE = $(filter %xdoc/Makefile.inc,$(MAKEFILE_LIST))

XDOC_DIR = $(patsubst %/Makefile.inc,%,$(XDOC_MAKEFILE))

DOC_DIR = $(abspath .)

T:=$(XDOC_DIR)/texinput


APPS_ROOT     ?= $(abspath $(XDOC_DIR)/..)
SPHINXOPTS    =
SPHINXBUILD   = python $(XDOC_DIR)/xsphinx/sphinx-build.py
PAPER         =
BUILDDIR      = _build
DOXYGEN_DIRS  ?=
#SOURCE_INCLUDE_DIRS ?=
SPHINX_MASTER_DOC ?= index
SPHINX_SECTION_NEWPAGE ?= 1

export XDOC_DIR
export SPHINX_PROJECT_NAME
export VERSION
export DOC_DIR
export DOXYGEN_DIRS
export SOURCE_INCLUDE_DIRS
export SPHINX_LATEX_DOCTYPE
export SPHINX_MASTER_DOC
export SPHINX_SECTION_NEWPAGE
export BREADCRUMB_PREFIX
export USE_COMMENTS
export EXTRACONF
export

PYTHONPATH_EXTRA:=:$(XDOC_DIR)



%.doxygen:
	cp $(XDOC_DIR)/xsphinx/Doxyfile $*/Doxyfile
	cd $* && doxygen 2>&1 | grep -v "REFERENCE_PARAM"
	mkdir -p $(DOC_DIR)/_build/doxygen/$*
	cp -r $*/_doxygen_xml $(DOC_DIR)/_build/doxygen/$*/xml
	rm -rf $*/_doxygen_xml
	rm $*/Doxyfile

doxygen:
	@echo "Running Doxygen"
	@cp $(XDOC_DIR)/xsphinx/Doxyfile $(DOC_DIR)/Doxyfile
	@sed -i -e 's/--INPUT--/$(subst /,\/,$(DOXYGEN_DIRS))/g' Doxyfile
	@mkdir -p $(DOC_DIR)/_build/doxygen
	@export PATH=$(PATH):/tools/doxygen/doxygen-1.5.8/bin/ && cd $(DOC_DIR) && doxygen 2>&1 | grep -v "REFERENCE" ; echo "Done"
	@rm $(DOC_DIR)/Doxyfile

html: doxygen | $(LINKED_DIRS)
	export CURRENT_BUILDER=html && export PYTHONPATH=$(PYTHONPATH)$(PYTHONPATH_EXTRA) && $(SPHINXBUILD) -c $(XDOC_DIR)/xsphinx -b html $(ALLSPHINXOPTS) . $(BUILDDIR)/html
	@echo ".nojekyll" > _build/html/.nojekyll
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/html."



singlehtml: doxygen | $(LINKED_DIRS)
	export CURRENT_BUILDER=html && export PYTHONPATH=$(PYTHONPATH)$(PYTHONPATH_EXTRA) && $(SPHINXBUILD) -c $(XDOC_DIR)/xsphinx -b singlehtml $(ALLSPHINXOPTS) . $(BUILDDIR)/singlehtml
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/singlehtml."


xlatex: doxygen
	export CURRENT_BUILDER=$(XLATEX) && export PYTHONPATH=$(PYTHONPATH)$(PYTHONPATH_EXTRA) && $(SPHINXBUILD) -c $(XDOC_DIR)/xsphinx -b $(XLATEX) $(ALLSPHINXOPTS) . $(BUILDDIR)/$(XLATEX)
	cp _build/$(XLATEX)/*.tex .

man: doxygen | $(LINKED_DIRS)
	export PYTHONPATH=$(PYTHONPATH)$(PYTHONPATH_EXTRA) && $(SPHINXBUILD) -c $(XDOC_DIR)/xsphinx -b man $(ALLSPHINXOPTS) . $(BUILDDIR)/man
	@echo
	@echo "Build finished. The man pages are in $(BUILDDIR)/man."


.SUFFIXES: .tex .pdf .svg .jpg

%.jpg: %.svg
	inkscape -z -f $*.svg -d 300 -e $*.png
	convert $*.png $*.jpg


%.pdf: %.tex xlatex
	export TEXINPUTS=$(T):_build/$(XLATEX):; pdflatex $<;pdflatex $<

TEXROOT = $(subst /,_,$(subst $(space),_,$(call lc,$(SPHINX_PROJECT_NAME))))
PDF_TARGET = $(TEXROOT).pdf

pdf: XLATEX=xlatex
pdf: xlatex | $(LINKED_DIRS)
	@$(call DO_LATEX, $(TEXROOT).tex)
	@echo "Build complete"


latex_to_pdf:
	export TEXINPUTS=$(T):; pdflatex $(TEXROOT).tex;pdflatex $(TEXROOT).tex
	@echo "Build complete"

clean:
	rm -rf _build
	-rm -f $(TEXROOT).tex
	-rm -f $(TEXROOT).dvi
	-rm -f $(TEXROOT).pdf
	-rm -f $(TEXROOT).idx
	-rm -f $(TEXROOT).log
	-rm -f $(TEXROOT).out
	-rm -f $(TEXROOT).aux


-include $(APPS_ROOT)/infr_docs/Makefile.xdoc_extras
