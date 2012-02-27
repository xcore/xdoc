no_target:
	echo "Please enter target to build: pdf html xmospdf xmoshtml"

export

# Now just call Makefile.inc1
define DISPATCH
$1:
	@python $(XDOC_DIR)/xdoc.py $1
endef

$(foreach goal,$(sort html pdf xmoshtml xdehtml xmospdf justlatex xref all_xref cognidox draft issue webgen archive copy_remote xdetutorial xmospdf.remote xdehtml.remote),$(eval $(call DISPATCH,$(goal))))

clean:
	rm -rf .linked_dirs
	rm -rf .sources
	rm -rf .doxygen
	rm -rf _build
	rm -rf html
	rm -rf web-output
	-rm -f $(TEXROOT).toc$
	-rm -f $(TEXROOT).tex
	-rm -f $(TEXROOT).toc
	-rm -f $(TEXROOT).dvi
	-rm -f $(TEXROOT).pdf
	-rm -f $(TEXROOT).idx
	-rm -f $(TEXROOT).log
	-rm -f $(TEXROOT).out
	-rm -f $(TEXROOT).aux


realclean: clean
	-rm -rf .support
