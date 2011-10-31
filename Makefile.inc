export

RSYNC = rsync -tur --cvs-exclude --exclude=**.xe --exclude=**.zip --exclude=**_buid** --exclude=**.build**

# Need to copy in linked dirs before anything else
ifeq ($(OTHER_DOC_DIRS),)
LINKED_DIRS =
else
.PHONY: _linked_dirs

ifeq ($(NOCOPY),1)
_linked_dirs:
	@echo Not copying linked dirs
else

_linked:
	@-mkdir -p .linked_dirs

%._linked: _linked
	@echo Copying in $*
	$(RSYNC) --exclude=**.linked_dirs** $(abspath $*) .linked_dirs

_linked_dirs: $(foreach x,$(OTHER_DOC_DIRS),$(x)._linked)
	@python $(XDOC_DIR)/xsphinx/create_link_map.py $(OTHER_DOC_DIRS)
	@echo "Created linked dirs"
endif

LINKED_DIRS = _linked_dirs
endif


# Now just call Makefile.inc1
define DISPATCH
$1: $(LINKED_DIRS)
	@make --no-print-directory -f $(XDOC_DIR)/Makefile.inc1 $1
endef

$(eval $(foreach goal,$(MAKECMDGOALS),$(call DISPATCH,$(goal))))