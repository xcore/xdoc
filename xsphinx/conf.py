# -*- coding: utf-8 -*-
#
# xsphinx documentation build configuration file, created by
# sphinx-quickstart on Sun Oct 10 07:04:01 2010.
#
# This file is execfile()d with the current directory set to its containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.


import sys, os, re
from xsphinx.builders.xlatex import XLaTeXBuilder, xlatex_rearrange_tocs
import xsphinx.code
import xsphinx.images
import xcomment
import srcfile
import docutils
from docutils import nodes
import xroles
import xdirectives
from xsphinx.xdoctoctree import XdocTocTree
import xtable
import sphinx.domains.std
import xsphinx.passes


if 'USE_AAFIG' in os.environ:
    use_aafig = (os.environ['USE_AAFIG'] != '0')
else:
    use_aafig = False


if 'CURRENT_BUILDER' in os.environ:
    current_builder = os.environ['CURRENT_BUILDER']
else:
    current_builder = None




if 'USE_COMMENTS' in os.environ and os.environ['USE_COMMENTS']=='1':
    enable_comments = True
else:
    enable_comments = False

#keep_warnings = True

xsphinx_dir = os.environ['XDOC_DIR'] + "/xsphinx"

#short_name = os.environ['SPHINX_PROJECT_NAME'].lower()
#short_name = re.sub('[,:. /]','_',short_name)
short_name = os.path.split(os.environ['_SPHINX_MASTER_DOC'])[-1]

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#sys.path.insert(0, os.path.abspath('.'))

# -- General configuration -----------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#needs_sphinx = '1.0'

sys.path.append(xsphinx_dir + "/breathe")

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = ['sphinx.ext.ifconfig', 'xsphinx.ext.mathjax', 'breathe']

if use_aafig:
    print "Found and adding aafig extension"
    extensions.append('sphinxcontrib.aafig')

aafig_default_options = dict(proportional=True,width="100%",textual=True)


# Add any paths that contain templates here, relative to this directory.
templates_path = [xsphinx_dir + '/_templates']

mathjax_path = 'http://mathjax.connectmv.com/MathJax.js'

# The suffix of source filenames.
source_suffix = '.rst'

# The encoding of source files.
#source_encoding = 'utf-8-sig'

# The master toctree document.
if '_SPHINX_MASTER_DOC' in os.environ:
    master_doc = os.environ['_SPHINX_MASTER_DOC']
else:
    master_doc = 'index'


# General information about the project.
project = os.environ['SPHINX_PROJECT_NAME']
copyright = u''

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = ''#os.environ['VERSION']
# The full version, including alpha/beta/rc tags.
release = ''#os.environ['VERSION']

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#today = ''
# Else, today_fmt is used as the format for a strftime call.
#today_fmt = '%B %d, %Y'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.

exclude_patterns = [xsphinx_dir + '/_build','.*\.#.*']
exclude_patterns += ['.support*','.sources*','.doxygen*']
#,'_linked_dirs/.*/'+os.path.split(os.path.abspath(os.environ['DOC_DIR']))[1]+'.*']

exclude_dirnames = [os.path.split(os.path.abspath(os.environ['DOC_DIR']))[1]]
# The reST default role (used for this markup: `text`) to use for all documents.
#default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
#add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
#add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
#show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
#modindex_common_prefix = []


# -- Options for HTML output ---------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
 
html_theme = 'xdoc'
#html_theme = 'default'




# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
html_theme_options = {}


# Add any paths that contain custom themes here, relative to this directory.
doc_dir = os.path.abspath(os.environ['DOC_DIR'])
user_theme_dir = os.path.relpath(os.path.join(doc_dir,"themes"))
html_theme_path = ["themes",user_theme_dir]


# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
#html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
html_short_title = "%s"%(project)

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
#html_logo = None

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
#html_favicon = None

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = []

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
#html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
#html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.

default_sidebars = ['globaltoc.html', 'searchbox.html']

if enable_comments:
    default_sidebars.append('commentctl.html')

html_sidebars = {'**':default_sidebars}

# Additional templates that should be rendered to pages, maps page names to
# template names.
#html_additional_pages = {}

# If false, no module index is generated.
#html_domain_indices = True

# If false, no index is generated.
#html_use_index = True

# If true, the index is split into individual pages for each letter.
#html_split_index = False

# If true, links to the reST sources are added to the pages.
html_show_sourcelink = False

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
html_show_sphinx = False

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
html_show_copyright = False

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
#html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
#html_file_suffix = None

# Output file base name for HTML help builder.
htmlhelp_basename = short_name


# -- Options for LaTeX output --------------------------------------------------

latex_docclass = 'xcore'

try:
    latex_doctype = os.environ['SPHINX_LATEX_DOCTYPE']
except:
    latex_doctype = 'article'


if 'SPHINX_SECTION_NEWPAGE' in os.environ:
    latex_section_newpage = (os.environ['SPHINX_SECTION_NEWPAGE'] == '1')
else:
    latex_section_newpage = True

latex_toc = True

# The paper size ('letter' or 'a4').
#latex_paper_size = 'letter'

# The font size ('10pt', '11pt' or '12pt').

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
latex_documents = [
  (master_doc, short_name + '.tex', '', #os.environ['SPHINX_PROJECT_NAME'],
   u'', 'manual'),
]

latex_font_size = ''

# The name of an image file (relative to this directory) to place at the top of
# the title page.
#latex_logo = None

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
#latex_use_parts = False

# If true, show page references after internal links.
#latex_show_pagerefs = False

# If true, show URL addresses after external links.
#latex_show_urls = False

# Additional stuff for the LaTeX preamble.
#latex_preamble = ''

# Documents to append as an appendix to all manuals.
#latex_appendices = []

# If false, no module index is generated.
#latex_domain_indices = True


# -- Options for manual page output --------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    ('index', short_name, '',#os.environ['SPHINX_PROJECT_NAME'] ,
     [u'XCore'], 1)
]

#print os.environ['SOURCE_INCLUDE_DIRS']
include_search_dirs = os.environ['SOURCE_INCLUDE_DIRS'].split(' ')

include_search_dirs = [x for x in include_search_dirs if x != '']

#print include_search_dirs

class C:
    pass


primary_domain = None

if 'BREADCRUMB_PREFIX' in os.environ:
    breadcrumb_prefix = os.environ['BREADCRUMB_PREFIX']
else:
    breadcrumb_prefix = ""

if 'EXTRACONF' in os.environ:
    extraconf_modules = set(['extraconf'] + re.split('\W+',os.environ['EXTRACONF'].strip()))
else:
    extraconf_modules = set(['extraconf'])


class Configurator(object):
    def __init__(self):
        self._settings = {}

    def set_value(self, name, val):
        self._settings[name] = val

    def set_value_eval(self, name, val):
        self._settings[name] = "eval:" + val

    def set(self):
        for key, val in self._settings.items():                        
            if isinstance(val,str):
                if val[0:5] == "eval:":
                    cmd = "global %s;%s = %s" % (key, key, val[5:])
                else:
                    cmd = "global %s;%s = '%s'" % (key, key, val)
            else:
                cmd = "global %s;%s = %s" % (key, key, val) 
            exec(cmd)
        


def setup(app):
    global xmos_compact_pdf, collection, xmos_manual_pdf, latex_doctype
    global latex_section_numbers, latex_section_newpage, latex_toc
    global use_sidecaption, latex_use_chapters

    if 'XMOSCOMPACTPDF' in os.environ:
        xmos_compact_pdf = (os.environ['XMOSCOMPACTPDF'] == "1")
        collection = False
    else:
        xmos_compact_pdf = False
        collection = True

    if 'XMOSMANUALPDF' in os.environ:
        xmos_manual_pdf = (os.environ['XMOSMANUALPDF'] == "1")
    else:
        xmos_manual_pdf = False

    if xmos_compact_pdf:
        latex_doctype = 'document'
        latex_section_numbers = True
        latex_section_newpage = False
        latex_toc = False
        use_sidecaption = True
    elif xmos_manual_pdf:
        latex_doctype = 'collection'
        latex_section_numbers = True
        use_sidecaption = True
        latex_use_chapters = True
    else:
        latex_section_numbers = True


    app.add_builder(XLaTeXBuilder)
    if current_builder in ['xlatex']:
        app.connect('doctree-resolved',xlatex_rearrange_tocs)
    app.add_directive('literalinclude', xsphinx.code.LiteralInclude)
    app.add_directive('figure', xsphinx.images.Figure)
    app.add_directive('image', xsphinx.images.Image)
    app.add_directive('generalfigure', xdirectives.GeneralFigure)
    app.add_config_value('include_search_dirs',[],False)
    app.add_config_value('latex_doctype',[],False)
    app.add_config_value('latex_section_newpage',[],False)
    app.add_config_value('latex_section_numbers',[],True)
    app.add_config_value('latex_use_chapters',[],False)
    app.add_config_value('breadcrumb_prefix',[],False)
    app.add_config_value('use_xmoslatex',[],False)
    app.add_config_value('use_sidecaption',[],False)
    app.add_config_value('tiny_verbatim',[],False)
    app.add_config_value('latex_toc',True,False)
    app.add_config_value('body_only',False,'')
    app.add_config_value('collection',False,'')

    app.add_generic_role('srcfile',docutils.nodes.literal)
    app.add_generic_role('~',docutils.nodes.term)
    app.add_generic_role('n',docutils.nodes.term)
    app.add_directive('squeeze',xdirectives.SqueezeDirective)
    app.add_directive('toctree', XdocTocTree)
    app.add_directive('table', xtable.Table)
    app.add_role("sub",xroles.subscript)
    app.add_role("sup",xroles.superscript)
    app.add_role("command",xroles.command)
    app.add_role("tt",xroles.tt)
    app.connect('doctree-resolved',xsphinx.passes.format_references)
    app.connect('doctree-resolved',xlatex_rearrange_tocs)


    app.add_node(xdirectives.newinxc)

    app.add_directive("newinxc", xdirectives.NewInXCDirective)
    app.add_directive("steps", xdirectives.Steps)
    app.add_directive("nopoints", xdirectives.NoPoints)
    app.add_directive("points", xdirectives.Points)
    app.add_directive("actions", xdirectives.Actions)
    app.add_directive("xoption", xdirectives.Cmdoption)
    app.add_directive("commentary", xdirectives.Commentary)
    app.add_directive("toolsoutput", xdirectives.ToolsOutput)
    app.add_directive("ebnf", xdirectives.Ebnf)
    app.add_directive("paragraph-headings", xdirectives. ParagraphHeadingList)
    app.add_role("ebnf",xdirectives.ebnf_role)


    xcomment.setup(app, enable_comments)

    try:
        __import__('xmosconf')
        extraconf_modules.add('xmosconf')
    except:
        pass

    for mod in extraconf_modules:
        mod = mod.strip()
        if len(mod) > 0:
            try:
                mod = __import__(mod)
            except ImportError:
                pass
            else:
                conf = Configurator()
                extra_setup = getattr(mod, 'setup')
                extra_setup(app, conf, tags)
                conf.set()

    app.add_role("menuitem",xdirectives.make_menuitem(current_builder))

# -- Options for breathe --

breathe_projects = { 'auto_doxygen' : '_build/doxygen/xml' }
breathe_default_project = 'auto_doxygen'

rst_prolog = '''
.. highlight:: none

'''


if current_builder=='xlatex':
        rst_epilog = '''

.. |submenu| raw:: latex
 
         \\submenu

.. |micro| raw:: latex
 
         \\micro

.. |newpage| raw:: latex

               \\newpage

.. |sect| raw:: latex

             \\S

.. |plusmn| raw:: latex

             $\\pm$

.. |infinity| raw:: latex

             $\\infty$


.. |cloverleaf| raw:: latex

             \\CloverLeaf
			 
.. |ne| raw:: latex

             $\\ne$

.. |reddot| raw:: latex

             {\\color{red}{\\LARGE\\textbullet}}

.. |amberdot| raw:: latex

             {\\color{xmosyellow}{\\LARGE\\textbullet}}

.. |greendot| raw:: latex

             {\\color{green}{\\LARGE\\textbullet}}

        '''
else:
        rst_epilog = """
.. |submenu| replace:: **>**

.. |micro| raw:: html

             &micro;

.. |newpage|  raw:: latex

               \\newpage

.. |sect| raw:: html

             &sect;

.. |plusmn| raw:: html

             &plusmn;

.. |infinity| raw:: html

             &#8734;

.. |cloverleaf| raw:: html

             &cloverleaf;

.. |ne| raw:: html

             &ne;

.. |reddot| raw:: html

             <span class="red">&bull;</span>

.. |amberdot| raw:: html

            <span class="amber">&bull;</span>

.. |greendot| raw:: html

            <span class="green">&bull;</span>

        """

rst_epilog += """
.. |-| replace:: ihjsqueezeihj

.. |beginmbox| raw:: latex

              \\mbox{

.. |endmbox| raw:: latex

              }

"""
