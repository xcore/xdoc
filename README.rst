XDoc: common documentation infrastructure
.........................................

:Last Release:  unreleased
:Status:     in development
:Maintainer:   Dave Lacey (github: davelxmos)


Key Features
============

   * Adaptation of sphinx documentation system for documenting XC/C
     projects
   * Incorporation of doxygen comments (using breathe_)
   
Overview
========

This repository does not contain any code. It contains the common
Makefile and scripts to build documentation for other repositories.

The documentation basically uses sphinx with the following additions:

   * Themes/writers are provided for html and latex to maintain
     consistency across repos
   * An adapted version of breathe_ is provided to link doxygen
     comments into the documentation
   * Makefiles etc. to link it all together and be able to pull 
     out source/comments from source in different repositories

You can find examples using this repository in:

  * http://www.github.com/xcore/sc_ethernet
  * http://www.github.com/xcore/sc_xtcp
  * http://www.github.com/xcore/doc_tips_and_tricks

In each case the doc/ directory has a Makefile which can build with
the targets ``make html`` or ``make pdf``.

Known Issues
============

None

Requirements
============

You need the following installed to build the documentation (the versions in brackets are know to work):

  * Python (http://www.python.org/)  (2.6.5)
  * Sphinx (http://sphinx.pocoo.org/) (1.0.7)
  * Docutils (http://docutils.sourceforge.net/) (0.6)
  * Doxygen (http://www.stack.nl/~dimitri/doxygen/index.html) (1.6.3)
  * LaTeX, if you want to build PDFs (http://www.latex-project.org/) 
  * Gnu Make (xmake will work)

You do not need to install breathe since an adapted version is
included in this repository. 
Currently, building documentation has only been done on
Linux variants. However, everything used is cross platform.

Support
=======

Issues may be submitted via the Issues tab in this github repo. Response to any issues submitted as at the discretion of the manitainer for this line.

.. _breathe: http://github.com/michaeljones/breathe
