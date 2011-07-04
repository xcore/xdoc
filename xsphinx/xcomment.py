from docutils import nodes
from sphinx.util.compat import Directive
from docutils.parsers.rst import directives
import os, subprocess

class Slot(object):

    def __init__(self, num, doc, line):
        self.num = num
        self.line = line
        self.doc = doc
        self.comments = []




class comment(nodes.General, nodes.Element):

    def __init__(self, date, author):
        self.date = date
        self.author = author
        super(comment, self).__init__()
    
def add_comment_slots(app, doctree, fromdocname):
    env = app.builder.env
    if not hasattr(env,'comment_slot_count'):
        env.comment_slot_count = 0
    if not hasattr(env,'comment_count'):
        env.comment_count = 0

    for node in doctree.traverse(lambda n: isinstance(n,nodes.paragraph) or
                                           isinstance(n,comment)):
        if isinstance(node, comment):
            node.num = env.comment_count
            if hasattr(env,'last_slot'):
                env.last_slot.comments.append(node)
                node.slot = env.last_slot
            else:
                node.slot = None
            env.comment_count += 1
            node.parent.remove(node)

        elif not hasattr(node,'in_comment') or not node.in_comment:
            env.comment_slot_count += 1
            cs = Slot(env.comment_slot_count, 
                      fromdocname, 
                      node.line)
            env.last_slot = cs
            node.comment_slot = cs
        else:
            node.comment_slot = None

xcomment_form = """
<div id="xcomment-form-%(slot)d" class="xcomment-form">
<form id="xcomment-form-form-%(slot)d" action="../../xcomment_web.py/submit_comment" method="post">
<input type="hidden"  id="xcomment-input-line-%(slot)d" name="line" value="%(line)d"/>
<input type="hidden"  id="xcomment-input-page-%(slot)d" name="page" value="%(page)s"/>
<input type="hidden"  id="xcomment-input-doc-%(slot)d" name="doc" value="%(doc)s"/>
<input type="hidden"  id="xcomment-input-slotid-%(slot)d" name="slot_id" value="%(slot)d"/>
<table width="100%%">
	<colgroup><col align="left"></col><col align="left"></col></colgroup>  
	<tr><th>Name:</th>
		<td><input id="xcomment-input-name-%(slot)d" width="100%%" type="text" name="name" value="" title="name"><td></tr>
	<tr><th>Email:</th>
		<td><input id="xcomment-input-email-%(slot)d" width="100%%" type="text" name="email" title="email"><td></tr>

	<tr><th>Comment:</th>
		<td><textarea width="100%%" id="xcomment-input-comments-%(slot)d" name="comments" rows="3" cols="40" title="comments"></textarea></td></tr>
	<tr><td></td><td><input id="xcomment-submit-%(slot)d" type="submit" value="Send"> <input type="reset" id="reset"></td></tr>
</table>
</form>
</div>
"""

def depart_paragraph(self, node, parent_fn):    
    if not self.builder.config.enable_comments:
        parent_fn(self, node)
        return

    if hasattr(node,'comment_slot'):
        slot = node.comment_slot
    else:
        slot = None

    if slot: 
        num_comments = len(slot.comments)
        self.body.append('<!-- comment slot %s/%s -->'%(slot.doc, slot.line)) 
        if num_comments == 0:
            self.body.append('\n<span id="xcomment-inline-add-%d" class="xcomment-slot">'%slot.num)
            self.body.append('<a class="xcomment-inline-add-link" href="#" onclick="show_comment_form(%d);return false;">'%slot.num)
            self.body.append('add comment')
            self.body.append('</a></span>\n')
        else:
            if num_comments == 1:
                comment_plural = "comment"
            else:
                comment_plural = "comments"

            self.body.append('<span id="xcomment-expand-%d" class="xcomment-slot">'%slot.num)
            self.body.append('<a href="#" onclick="show_comments(%d);return false;">'%slot.num)
            self.body.append('%s %s'%(num_comments,
                                      comment_plural))
            self.body.append('</a></span>')

    parent_fn(self, node)

    if slot:
        for comment in slot.comments:
            comment.walkabout(self)

        self.body.append('\n<div class="xcomment-insert-point" id="xcomment-insert-point-%s"></div>\n'%slot.num)
            
        
        self.body.append(xcomment_form % {'slot':slot.num,
                                          'line':slot.line,
                                          'page':self.builder.current_docname,
                                          'doc':self.builder.config.xcomment_docpath})

        if num_comments != 0:
            self.body.append('<div id="xcomment-post-%d" class="xcomment-post">'%slot.num)    

            self.body.append('<span id="xcomment-post-add-%d" class="xcomment-post-comments">'%slot.num)
            self.body.append('<a href="#" href="#" onclick="show_comment_form(%d);return false;">'%slot.num)
            self.body.append('add comment')
            self.body.append('</a></span>')            
        else:
            self.body.append('<div id="xcomment-post-form-only-%d" class="xcomment-post">'%slot.num)        

        self.body.append('<span id="xcomment-post-hide-%d" class="xcomment-post-comments">'%slot.num)
        self.body.append('<a href="#" onclick="hide_comments(%d);return false;">'%slot.num)
        self.body.append('hide comments')
        self.body.append('</a></span>')

        self.body.append('</div>\n')
            


class CommentDirective(Directive):           

    has_content = True
    required_arguments = 0
    option_spec = {'date':directives.unchanged,
                   'author':directives.unchanged,
                   'email':directives.unchanged}
    
    def run(self):
        c = comment(self.options['date'],self.options['author'])
        self.state.nested_parse(self.content, self.content_offset,
                                c)
        for node in c.traverse(nodes.paragraph):
            node.in_comment = True

        return [c]


def visit_comment(self, node):
    if self.builder.config.enable_comments:
        if hasattr(node,'num') and node.slot:
            self.body.append('<div id="xcomment-%d-%d" class="xcomment">'%(node.slot.num, node.num))
            self.body.append('<div class="xcomment-header"><b>%s</b> - %s</div>'
                             %(node.author, node.date))


def depart_comment(self, node):
    if hasattr(node,'num'):
        self.body.append('</div>')

def setup(app, enable_comments):        
#    try:

    p =  subprocess.Popen(['git','rev-parse','--show-toplevel'],
                          stdout=subprocess.PIPE)
    p.wait()
    output = p.stdout.readlines()
    if len(output) > 0:
        _, toplevel = os.path.split(output[0].strip())
    else:
        toplevel = None

    p =  subprocess.Popen(['git','rev-parse','--show-prefix'],
                          stdout=subprocess.PIPE)
    p.wait()
    output = p.stdout.readlines()
    if toplevel and len(output) > 0:
        path = os.path.join(toplevel, output[0].strip())
    else:
        path = None



    app.add_config_value('enable_comments',enable_comments,False)
    app.add_config_value('xcomment_docpath',path,False)
    app.connect('doctree-resolved',add_comment_slots)
    app.add_node(comment,
                 html = (visit_comment, depart_comment))
    from sphinx.writers.html import HTMLTranslator as translator
    fn = translator.depart_paragraph
    setattr(translator,
            'depart_paragraph',
            lambda self, node: depart_paragraph(self, node, fn))
    app.add_directive('comment', CommentDirective)
