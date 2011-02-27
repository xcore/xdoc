
from breathe.renderer.rst.doxygen.base import Renderer
from breathe.renderer.rst.doxygen import xmosbreathe
from docutils import nodes
from docutils.statemachine import StringList
class DoxygenTypeSubRenderer(Renderer):

    def render(self):

        compound_renderer = self.renderer_factory.create_renderer(self.data_object.compounddef, self.state, self.content, self.content_offset)
        return compound_renderer.render()


class CompoundDefTypeSubRenderer(Renderer):

    section_titles = [
                ("user-defined", "User Defined"),
                ("public-type", "Public Type"),
                ("public-func", "Public Functions"),
                ("public-attrib", "Public Members"),
                ("public-slot", "Public Slot"),
                ("signal", "Signal"),
                ("dcop-func",  "DCOP Function"),
                ("property",  "Property"),
                ("event",  "Event"),
                ("public-static-func", "Public Static Functons"),
                ("public-static-attrib", "Public Static Attributes"),
                ("protected-type",  "Protected Types"),
                ("protected-func",  "Protected Functions"),
                ("protected-attrib",  "Protected Attributes"),
                ("protected-slot",  "Protected Slots"),
                ("protected-static-func",  "Protected Static Functions"),
                ("protected-static-attrib",  "Protected Static Attributes"),
                ("package-type",  "Package Types"),
                ("package-attrib", "Package Attributes"),
                ("package-static-func", "Package Static Functions"),
                ("package-static-attrib", "Package Static Attributes"),
                ("private-type", "Private Types"),
                ("private-func", "Private Functions"),
                ("private-attrib", "Private Members"),
                ("private-slot",  "Private Slots"),
                ("private-static-func", "Private Static Functions"),
                ("private-static-attrib",  "Private Static Attributes"),
                ("friend",  "Friends"),
                ("related",  "Related"),
                ("define",  "Defines"),
                ("prototype",  "Prototypes"),
                ("typedef",  "Typedefs"),
                ("enum",  "Enums"),
                ("func",  "Functions"),
                ("var",  "Variables"),
                ("enumvalue", "Enum Values")
             ]


    def extend_nodelist(self, nodelist, section, title, section_nodelists):

        # Add title and contents if found
        if section_nodelists.has_key(section):
            nodelist.append(self.node_factory.emphasis(text=title))
            nodelist.append(self.node_factory.block_quote("", *section_nodelists[section]))

    def render(self):


        section_nodelists = {}

        # Get all sub sections
        for sectiondef in self.data_object.sectiondef:
            kind = sectiondef.kind

            renderer = self.renderer_factory.create_renderer(sectiondef, self.state, self.content, self.content_offset)
            subnodes = renderer.render()
            section_nodelists[kind] = subnodes
                                               
        nodelist = []    

        if self.data_object.briefdescription:
            renderer = self.renderer_factory.create_renderer(self.data_object.briefdescription,self.state, self.content, self.content_offset)
            nodelist.append(self.node_factory.paragraph("", "", *renderer.render()))

        if self.data_object.detaileddescription:
            renderer = self.renderer_factory.create_renderer(self.data_object.detaileddescription,self.state, self.content, self.content_offset)
            nodelist.append(self.node_factory.paragraph("", "", *renderer.render()))

        # Order the results in an appropriate manner
        for entry in self.section_titles:
            self.extend_nodelist(nodelist, entry[0], entry[1], section_nodelists)

        self.extend_nodelist(nodelist, "", "", section_nodelists)

        return [self.node_factory.block_quote("", *nodelist)]


class SectionDefTypeSubRenderer(Renderer):

    def render(self):

        defs = []

        # Get all the memberdef info
        for memberdef in self.data_object.memberdef:
            renderer = self.renderer_factory.create_renderer(memberdef,self.state, self.content, self.content_offset)
            defs.extend(renderer.render())

        if defs:
            return [self.node_factory.definition_list("", *defs)]

        # Return with information about which section this is
        return []

class MemberDefTypeSubRenderer(Renderer):

    def render(self):
        return xmosbreathe.render(self.data_object,
                                  self.state,
                                  self.content,
                                  self.content_offset)
        
#        env = self.document.settings.env
#        fdir = env.lookup_domain_element('directive', 'c:function')[0]
#        term = nodes.term()
#        n = nodes.strong(text=self.data_object.name) 

#        term += n
#        return [term]

#        para = nodes.paragraph()
        str = ".. c:function:: %s" % (self.data_object.name)

        print self.data_object.kind
        if self.data_object.kind == "function":
            str = ".. c:function:: " + self.data_object.definition + self.data_object.argsstring.replace("&amp","&")

            #str += "("
            # Get the function arguments
            for i, parameter in enumerate(self.data_object.param):
                #if i: str += ", "
                print parameter.declname
#                print dir(parameter)
                typ = parameter.type_.content_[0].getValue()
                print typ
                #str += parameter.declname

        
#        content = self.document._current_content
        self.content.data = str.split("\n")
        print self.content
#        block = StringList(initlist=str.split("\n"))
        defn = nodes.term()
        self.state.nested_parse(self.content, self.content_offset, defn)
        return [defn]
        #print self.data_object.kind
        
        print self.document._current_state


        kind = []
        
        # Variable type or function return type
        if self.data_object.type_:
            renderer = self.renderer_factory.create_renderer(self.data_object.type_,self.state, self.content, self.content_offset)
            kind = renderer.render()
    
        name = self.node_factory.strong(text=self.data_object.name)

        args = []
        args.extend(kind)
        args.extend([self.node_factory.Text(" "), name])

        # This test should be done in the RendererFactory
        if self.data_object.kind == "function":

            # Get the function arguments
            args.append(self.node_factory.Text("("))
            for i, parameter in enumerate(self.data_object.param):
                if i: args.append(self.node_factory.Text(", "))
                renderer = self.renderer_factory.create_renderer(parameter,self.state, self.content, self.content_offset)
                args.extend(renderer.render())
            args.append(self.node_factory.Text(")"))

        term = self.node_factory.term("","", *args)

        description_nodes = []

        if self.data_object.briefdescription:
            renderer = self.renderer_factory.create_renderer(self.data_object.briefdescription,self.state, self.content, self.content_offset)
            description_nodes.append(self.node_factory.paragraph("", "", *renderer.render()))

        if self.data_object.detaileddescription:
            renderer = self.renderer_factory.create_renderer(self.data_object.detaileddescription,self.state, self.content, self.content_offset)
            description_nodes.append(self.node_factory.paragraph( "", "", *renderer.render()))


        definition = self.node_factory.definition("", *description_nodes)

        refid = "%s%s" % (self.project_info.name(), self.data_object.id)
        #refid = refid.replace("_8c","_8h")
        print "t:" + refid + ":(" + str(name) + ")"
        target = self.node_factory.target('','',refid=refid, ids=[self.node_factory.make_id(refid)], names=[self.node_factory.fully_normalize_name(refid)])

        # Tell the document about our target
        try:
            self.document.note_explicit_target(target, target)
        except Exception, e:
            print "Failed to register id: %s. It is probably a duplicate." % refid

        deflist = self.node_factory.definition_list()
        deflist += self.node_factory.definition_list_item("",term, definition)
        # Build the list item
        nodelist = [target, deflist]
#        nodelist = [target, self.node_factory.definition_list_item("",term, definition)]

        return nodelist


class DescriptionTypeSubRenderer(Renderer):

    def render(self):

        nodelist = []
        
        # Get description in rst_nodes if possible
        for item in self.data_object.content_:
            renderer = self.renderer_factory.create_renderer(item,self.state, self.content, self.content_offset)
            nodelist.extend(renderer.render())

        return nodelist


class LinkedTextTypeSubRenderer(Renderer):

    def render(self):

        nodelist = []

        # Recursively process where possible
        for i in self.data_object.content_:
            renderer = self.renderer_factory.create_renderer(i,self.state, self.content, self.content_offset)
            nodelist.extend(renderer.render())
            nodelist.append(self.node_factory.Text(" "))


        return nodelist


class ParamTypeSubRenderer(Renderer):

    def render(self):

        nodelist = []

        # Parameter type
        if self.data_object.type_:
            renderer = self.renderer_factory.create_renderer(self.data_object.type_,self.state, self.content, self.content_offset)
            nodelist.extend(renderer.render())

        # Parameter name
        if self.data_object.declname:
            nodelist.append(self.node_factory.Text(self.data_object.declname))

        if self.data_object.defname:
            nodelist.append(self.node_factory.Text(self.data_object.defname))

        # Default value
        if self.data_object.defval:
            nodelist.append(self.node_factory.Text(" = "))
            renderer = self.renderer_factory.create_renderer(self.data_object.defval,self.state, self.content, self.content_offset)
            nodelist.extend(renderer.render())

        return nodelist


class DocRefTextTypeSubRenderer(Renderer):

    def render(self):

        nodelist = []

        for item in self.data_object.content_:
            renderer = self.renderer_factory.create_renderer(item,self.state, self.content, self.content_offset)
            nodelist.extend(renderer.render())

        refid = "%s%s" % (self.project_info.name(), self.data_object.refid)
        #refid = refid.replace("_8c","_8h")
        print "r:" + refid + ":"
        nodelist = [
                self.node_factory.pending_xref(
                    "",
                    reftype="ref",
                    refid=refid, 
                    refdoc=None,
                    reftarget=refid,
                    refcaption=refid,
                    *nodelist
                    )
                ]

        return nodelist

class DocParaTypeSubRenderer(Renderer):

    def render(self):

        nodelist = []
        for entry in self.data_object.parameterlist:
            renderer = self.renderer_factory.create_renderer(entry,self.state, self.content, self.content_offset)
            nodelist.extend(renderer.render())

        for item in self.data_object.content:
            renderer = self.renderer_factory.create_renderer(item,self.state, self.content, self.content_offset)
            nodelist.extend(renderer.render())

        def_list_items = []
        for item in self.data_object.simplesects:
            renderer = self.renderer_factory.create_renderer(item,self.state, self.content, self.content_offset)
            def_list_items.extend(renderer.render())

        if def_list_items:
            nodelist.append(self.node_factory.definition_list("", *def_list_items))
        
        return nodelist

class DocParamListTypeSubRenderer(Renderer):

    lookup = {
            "param" : "Parameters",
            "exception" : "Exceptions",
            }

    def render(self):

        nodelist = []
        for entry in self.data_object.parameteritem:
            renderer = self.renderer_factory.create_renderer(entry,self.state, self.content, self.content_offset)
            nodelist.extend(renderer.render())

        name = self.lookup[self.data_object.kind]
        title = self.node_factory.emphasis("", self.node_factory.Text(name))

        return [title,self.node_factory.bullet_list("", *nodelist)]



class DocParamListItemSubRenderer(Renderer):

    def render(self):

        nodelist = []
        for entry in self.data_object.parameternamelist:
            renderer = self.renderer_factory.create_renderer(entry,self.state, self.content, self.content_offset)
            nodelist.extend(renderer.render())

        term = self.node_factory.literal("","", *nodelist)

        separator = self.node_factory.Text(" - ")

        nodelist = []

        if self.data_object.parameterdescription:
            renderer = self.renderer_factory.create_renderer(self.data_object.parameterdescription,self.state, self.content, self.content_offset)
            nodelist.extend(renderer.render())

        return [self.node_factory.list_item("", term, separator, *nodelist)]

class DocParamNameListSubRenderer(Renderer):

    def render(self):

        nodelist = []
        for entry in self.data_object.parametername:
            renderer = self.renderer_factory.create_renderer(entry,self.state, self.content, self.content_offset)
            nodelist.extend(renderer.render())

        return nodelist

class DocParamNameSubRenderer(Renderer):

    def render(self):

        nodelist = []
        for item in self.data_object.content_:
            renderer = self.renderer_factory.create_renderer(item)
            nodelist.extend(renderer.render())

        return nodelist

class DocSect1TypeSubRenderer(Renderer):

    def render(self):

        return []


class DocSimpleSectTypeSubRenderer(Renderer):

    def render(self):

        text = self.node_factory.Text(self.data_object.kind.capitalize())
        emphasis = self.node_factory.emphasis("", text)
        term = self.node_factory.term("","", emphasis)

        nodelist = []
        for item in self.data_object.para:
            renderer = self.renderer_factory.create_renderer(item)
            nodelist.append(self.node_factory.paragraph("", "", *renderer.render()))

        definition = self.node_factory.definition("", *nodelist)

        return [self.node_factory.definition_list_item("", term, definition)]


class MixedContainerRenderer(Renderer):

    def render(self):

        renderer = self.renderer_factory.create_renderer(self.data_object.getValue(),self.state, self.content, self.content_offset)
        return renderer.render()


