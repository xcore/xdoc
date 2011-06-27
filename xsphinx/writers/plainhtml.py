from sphinx.writers.html import SmartyPantsHTMLTranslator
from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.locale import admonitionlabels, versionlabels, _
from docutils import nodes

class plainhtml_builder(StandaloneHTMLBuilder):
    name = 'plainhtml'


class plainhtml_translator(SmartyPantsHTMLTranslator):
    """
    Subclasses the HTML translator
    """
    def __init__(self, *args, **kwds):
        self.in_toc = False
        SmartyPantsHTMLTranslator.__init__(self, *args, **kwds)


    def visit_title(self, node):
        source = self.document.children[0].source
        partial = source == '<partial node>'
        h_level = self.section_level + self.initial_header_level - 1
        h1 = h_level == 1 or isinstance(node.parent, nodes.document)
        if not partial and h1:
            raise nodes.SkipNode
        SmartyPantsHTMLTranslator.visit_title(self, node)


    def visit_list_item(self, node):
        self.body.append(self.starttag(node, 'li', ''))
        if len(node):
            node[0]['classes'].append('first')

    def depart_list_item(self, node):
        self.body.append('</li>\n')

    def visit_bullet_list(self, node):
        source = self.document.children[0].source
        partial = source == '<partial node>'
        is_toc = False
        for child in iter(node):
            for x in child['classes']:
                if x[0:3] == 'toc':
                    is_toc = True
        if is_toc and not partial:
            raise nodes.SkipNode
#        print dir(self.document.children[0])
        atts = {}
        old_compact_simple = self.compact_simple
        self.context.append((self.compact_simple, self.compact_p))
        self.compact_p = None
        self.compact_simple = self.is_compactable(node)
        if self.compact_simple and not old_compact_simple:
            atts['class'] = 'simple'



        if is_toc and not self.in_toc:
            atts['class'] = 'toc'
            node['ids'] = ['toc']
            node.toc_hdr = True
            self.in_toc = True
        else:
            node.toc_hdr = False
        
        self.body.append(self.starttag(node, 'ul', **atts))

    def depart_bullet_list(self, node):
        self.compact_simple, self.compact_p = self.context.pop()
        self.body.append('</ul>\n')
        if node.toc_hdr:
            self.in_toc = False

    def visit_admonition(self, node, name=''):
        self.body.append(self.starttag(
            node, 'p', CLASS=('admonition ' + name)))
        if name and name != 'seealso':
            node.insert(0, nodes.title(name, admonitionlabels[name]))
        self.set_first_last(node)


    def depart_admonition(self, node=None):
        self.body.append('</p>\n')


class FindPage(nodes.SparseNodeVisitor):

    def depart_bullet_list(self, node):        
        if isinstance(node.parent, nodes.list_item):
            page = node.parent[0][0].get('refuri')
            if not self.root and not page or page=="":
                self.root = node

        if len(node) == 0:
            if self.root == node:
                self.root == None
            node.parent.remove(node)
           
    def depart_list_item(self, node):
        refuri = node[0][0].get('refuri')
        if not refuri:
            refuri = node[0].get('refuri')
        if refuri and refuri.find('#') != -1:
            node.parent.remove(node)


def html_page_context(app, pagename, templatename, context, doctree):
    builder = app.builder
    env = builder.env
    context['breadcrumb_prefix'] = app.builder.config.breadcrumb_prefix
    if doctree:
        toc = env.get_toctree_for(pagename, builder, collapse=False)
        fp = FindPage(doctree)
        fp.pagename = pagename
        fp.root = None
        if toc:
            toc.walkabout(fp)
        if pagename == builder.config.master_doc:
            html = builder.render_partial(toc)['fragment']
        elif fp.root:
            html = builder.render_partial(fp.root)['fragment']
        else:            
            html = "" 
            
        
        context['ltoc'] = html
        
