no_target:
	echo "Please enter target to build: pdf html xmospdf xmoshtml"

export

# Now just call Makefile.inc1
define DISPATCH
$1:
	@python $(XDOC_DIR)/xdoc.py $1
endef

$(foreach goal,$(sort html pdf xmoshtml xdehtml xmospdf justlatex xref all_xref cognidox draft issue clean realclean webgen archive copy_remote xdetutorial xmospdf.remote xdehtml.remote),$(eval $(call DISPATCH,$(goal))))