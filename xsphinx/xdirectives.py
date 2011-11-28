
import os
import subprocess
import re
import sys

from docutils import nodes, utils
from sphinx.util.compat import Directive
from docutils.parsers.rst import directives
import docutils.parsers.rst.directives.tables
from sphinx import addnodes
from sphinx.util.nodes import split_explicit_title
from sphinx.locale import _
from sphinx.util import ws_re
import xsphinx
from sphinx.directives import ObjectDescription
from sphinx import addnodes
from sphinx.locale import l_, _
from sphinx.util.compat import make_admonition

class squeeze(nodes.General, nodes.Element):
    pass


class SqueezeDirective(Directive):

    has_content = False

    def run(self):
        return [squeeze()]

class general_figure(nodes.Element):
    pass

class GeneralFigure(Directive):

    has_content = True

    def run(self):
        fig = general_figure()
        self.state.nested_parse(self.content, self.content_offset, fig)
        if len(fig) < 1 or not isinstance(fig[0],nodes.paragraph):
            print >>sys.stderr, "ERROR: first paragraph of generalfigure should be present for the caption"
            return []

        first_para = fig[0]

        cap = nodes.caption()
        for c in first_para.children:
            cap.append(c.deepcopy())

        txt = cap.astext().strip()
        if re.match('[Tt]he.*',txt):
            print >>sys.stderr, "WARNING: Style: Caption '%s' begins with 'The'" % txt

        fig.remove(first_para)
        fig.append(cap)
        return [fig]



class newinxc(nodes.Admonition, nodes.Element):
    pass


class Steps(Directive):
    has_content = True

    option_spec = {'class': directives.class_option}

    def run(self):
        inline = nodes.inline()
        self.state.nested_parse(self.content, self.content_offset,
                                inline)
        if len(inline) < 1 or not isinstance(inline[0],nodes.enumerated_list):
            sys.stderr.write("ERROR: steps directive must contain enumerated list\n")
            exit(1)

        steps = inline[0]

        steps['classes'].append('steps')
        if 'class' in self.options:
            steps['classes'].extend(self.options['class'])

        return [inline]


class NoPoints(Directive):
    has_content = True

    option_spec = {'class': directives.class_option}

    def run(self):
        inline = nodes.inline()
        self.state.nested_parse(self.content, self.content_offset,
                                inline)
        if not isinstance(inline[0],nodes.bullet_list):
            sys.stderr.write("ERROR: nopoints directive must contain bullet list\n")
            exit(1)

        nopoints = inline[0]

        nopoints['classes'].append('nopoints')
        if 'class' in self.options:
            nopoints['classes'].extend(self.options['class'])

        return [inline]

class Points(Directive):
    has_content = True

    option_spec = {'class': directives.class_option}

    def run(self):
        inline = nodes.inline()
        self.state.nested_parse(self.content, self.content_offset,
                                inline)
        if not isinstance(inline[0],nodes.bullet_list):
            sys.stderr.write("ERROR: nopoints directive must contain bullet list\n")
            exit(1)

        points = inline[0]

        points['classes'].append('points')
        if 'class' in self.options:
            points['classes'].extend(self.options['class'])

        return [inline]


class Actions(Directive):
    has_content = True

    def run(self):
        inline = nodes.inline()
        self.state.nested_parse(self.content, self.content_offset,
                                inline)

        if len(inline) != 1 or not isinstance(inline[0],nodes.field_list):
            sys.stderr.write("ERROR: actions directive must contain field list\n")
            exit(1)

        # if not isinstance(inline[0],nodes.enumerated_list):
        #     sys.stderr.write("ERROR: steps directive must contain enumerated list\n")
        #     exit(1)

#        print inline[0]
        actions = inline[0]

        for field_list in inline.traverse(nodes.field_list):
            field_list['classes'].append('actions')

#        print(dir(steps))


        return [inline]

def make_menuitem(current_builder):
    def menuitem(role, rawtext, text, lineno, inliner, options={}, content={}):
        items = text.split(',')
        ret = []
        for i in range(len(items)):
            item = items[i]
            if current_builder == 'xdehtml':
                c = nodes.inline()

                n = nodes.Text(item)
#                print dir(n)
                c +=n
                if i != len(items)-1:
                    c['classes'].append('menuitem')
                else:
                    c['classes'].append('menuitemlast')
                ret.append(c)
            else:
                s = nodes.strong()
                s += nodes.Text(item)
                ret.append(s)
                if i != len(items)-1:
                    ret.append(nodes.Text(' '));
                    sub = nodes.substitution_reference()
                    sub['refname'] = 'submenu'
                    ret.append(sub)
        return ret, []
    return menuitem


# RE for option descriptions
option_desc_re = re.compile(
    r'((?:/|-|--)[-_a-zA-Z0-9]+)(\s*.*?)(?=,\s+(?:/|-|--)|$)')



class Cmdoption(ObjectDescription):
    """
    Description of a command-line option (.. cmdoption).
    """

    def handle_signature(self, sig, signode):
        """Transform an option description into RST nodes."""

        starts_with_arg = re.match(r'\s*\*',sig)

        options = sig.split("!")

        firstname = None
        for i in range(len(options)):
            o = options[i].strip()
            ws = o.split("*")
            if not firstname:
                firstname = ws[0]

            #is_name = not starts_with_arg
            is_name = True

            is_first_name = True
            for x in ws:
                if is_name:
                    n = addnodes.desc_name(x,x)
                    if is_first_name:
                        is_first_name = False
                        if i != 0:
                            n['classes'].append('duplicate')
                    signode += n
                    is_name = not is_name
                else:
                    signode += addnodes.desc_addname(x,x)
                    is_name = not is_name

        return firstname


    def add_target_and_index(self, name, sig, signode):
        targetname = name.replace('/', '-')
        currprogram = self.env.temp_data.get('std:program')
        if currprogram:
            targetname = '-' + currprogram + targetname
        targetname = 'cmdoption' + targetname
        signode['ids'].append(targetname)
        self.state.document.note_explicit_target(signode)
        self.indexnode['entries'].append(
            ('pair', _('%scommand line option; %s') %
             ((currprogram and currprogram + ' ' or ''), sig),
             targetname, ''))
        self.env.domaindata['std']['progoptions'][currprogram, name] = \
            self.env.docname, targetname


class NewInXCDirective(Directive):

    # this enables content in the directive
    has_content = True

    def run(self):
        env = self.state.document.settings.env
        ad = make_admonition(newinxc, self.name, [], self.options,
                             self.content, self.lineno, self.content_offset,
                             self.block_text, self.state, self.state_machine)


        return ad

class Commentary(Directive):
    has_content = True

    def run(self):
        bq = nodes.block_quote()
        self.state.nested_parse(self.content, self.content_offset,
                                bq)

        bq['classes'].append('commentary')

        return [bq]


class tools_output(nodes.Admonition, nodes.Element):
    pass


class ToolsOutput(Directive):
    has_content = True

    def run(self):
        lit = tools_output()

        txt = ''
        for x in self.content:
            txt += x+'\n'

        lit += nodes.Text(txt)

        return [lit]


class ebnf(nodes.General, nodes.Element):
    pass


def ebnf_role(role, rawtext, text, lineno, inliner, options={}, content={}):
    node = ebnf()
    node['classes'].append('inline')
    node.append(nodes.Text(rawtext[7:-1]))
    return [node],[]


class Ebnf(Directive):
    has_content = True

    option_spec = {'adjustindent':directives.unchanged}

    def run(self):
        lit = ebnf()


        txt = ''
        for x in self.content:
            txt += x+'\n'

        lit += nodes.Text(txt)

        if 'adjustindent' in self.options:
            lit['adjustindent'] = self.options['adjustindent']

        return [lit]

class ParagraphHeadingList(Directive):
    has_content = True

    def run(self):
        inline = nodes.container()
        self.state.nested_parse(self.content, self.content_offset,
                                inline)
        if len(inline) < 1 or not isinstance(inline[0],nodes.bullet_list):
            sys.stderr.write("ERROR: paragraph-headingss directive must contain a bullet list\n")
            return [nodes.Text("ERROR: paragraph-headingss directive must contain a bullet list\n")]

        lst = inline[0]

        for node in lst.children:
            for para in node.traverse(nodes.paragraph):
                para0 = nodes.paragraph()
                bnode = nodes.strong()
                para.replace_self(para0)
                bnode.append(para)
                para0.append(bnode)
                break

        return [inline]
