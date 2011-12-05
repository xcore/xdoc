no_target:
	echo "Please enter target to build: pdf html xmospdf xmoshtml"

export

RSYNC = rsync -tur --cvs-exclude --exclude=**.xe --exclude=**.zip --exclude=**_buid** --exclude=**.build** --exclude=**.sources**

# Need to copy in linked dirs before anything else
ifeq ($(OTHER_DOC_DIRS),)
_linked_dirs:
	@-mkdir -p .linked_dirs
	@python $(XDOC_DIR)/xsphinx/create_link_map.py $(OTHER_DOC_DIRS)

LINKED_DIRS = _linked_dirs
else
.PHONY: _linked_dirs

ifeq ($(NOCOPY),1)
_linked_dirs:
	@echo Not copying linked dirs
else

_linked:
	@-mkdir -p .linked_dirs

%.ignore:
	@echo Ignoring $*
	@rm `find .linked_dirs -iname $*`

%._linked: _linked
	@echo Copying in $*
	@$(RSYNC) --exclude=**.linked_dirs** $(abspath $*) .linked_dirs

_linked_dirs: $(foreach x,$(OTHER_DOC_DIRS),$(x)._linked) $(foreach x,$(EXCLUDE_FILES),$(x).ignore)
	@python $(XDOC_DIR)/xsphinx/create_link_map.py $(OTHER_DOC_DIRS)
	@echo "Created linked dirs"
endif

LINKED_DIRS = _linked_dirs
endif


# Now just call Makefile.inc1
define DISPATCH
$1: $(if $(filter clean,$1),,$(LINKED_DIRS))
	@make --no-print-directory -f $(XDOC_DIR)/Makefile.inc1 $1
endef

$(foreach goal,$(sort html pdf xmoshtml xmospdf justlatex xref all_xref cognidox draft issue clean realclean webgen),$(eval $(call DISPATCH,$(goal))))