from breathe.renderer.rst.doxygen import xmosbreathe
from breathe.renderer.rst.doxygen.base import Renderer

class DoxygenTypeSubRenderer(Renderer):

    def render(self):

        nodelist = []

        # Process all the compound children
        for compound in self.data_object.get_compound():
            compound_renderer = self.renderer_factory.create_renderer(compound, self.state, self.content, self.content_offset)
            nodelist.extend(compound_renderer.render())

        return nodelist


class CompoundTypeSubRenderer(Renderer):

    def __init__(self, compound_parser, *args):
        Renderer.__init__(self, *args)

        self.compound_parser = compound_parser

    def render(self):
         

        refid = "%s%s" % (self.project_info.name(), self.data_object.refid)
        #refid = refid.replace("_8c","_8h")
        target = self.node_factory.target(refid=refid, ids=[refid], names=[refid])

        # Tell the document about our target
        self.document.note_explicit_target(target)

        nodelist = [target]

        # Set up the title and a reference for it (refid)
        kind = self.node_factory.emphasis(text=self.data_object.kind)
        name = self.node_factory.strong(text=self.data_object.name)
        nodelist.append(
                self.node_factory.paragraph(
                    "",
                    "",
                    kind,
                    self.node_factory.Text(" "),
                    name,
                    ids=[refid]
                    )
            )

        # Read in the corresponding xml file and process
        file_data = self.compound_parser.parse(self.data_object.refid)
        data_renderer = self.renderer_factory.create_renderer(file_data, self.state, self.content, self.content_offset)

        return xmosbreathe.render_compoundtype(self.data_object, data_renderer.data_object, self.state, self.content, self.content_offset)
        #nodelist.extend(data_renderer.render())
        

        #return nodelist


