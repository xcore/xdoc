from breathe.parser.doxygen.compound import *
from breathe.parser.doxygen.compoundsuper import *
from docutils import nodes
import re
import sys
# This code is really strange since I'm refusing to follow what seem to be 
# some overly engineered design patterns in breathe but I'm not rewriting from 
# scratch either. The result is some rather hacky code

def add_indent(s):
    return ("\n".join(['    ' + x for x in s.split("\n")]) + "\n")


def render_param(data_object, tab):
    if hasattr(data_object,'parameterdescription'):
        name = render_content(data_object.parameternamelist[0], tab)
        desc = render_content(data_object.parameterdescription, tab)
        if desc[0] == '\n':
            desc = desc[1:]
        return ':param %s: %s\n\n' % (name, desc)
    else:
        return ''
    
def check_for_linked(x):
    if isinstance(x, linkedTextTypeSub):
        return True
    elif isinstance(x, MixedContainer):
        return check_for_linked(x.getValue())
    else:
        return False
        

def render_content(data_object, tab):
    tab += '   '
#    print tab + repr(data_object)
#    if isinstance(data_object, enumvalueTypeSub):
#    print tab + str(data_object)

    if isinstance(data_object, MixedContainer):
        s = render_content(data_object.getValue(), tab)
    else:
        s = ''
        
    if hasattr(data_object,'briefdescription'):
        s += render_content(data_object.briefdescription, tab)
    
    if hasattr(data_object,'detaileddescription'):
        s += render_content(data_object.detaileddescription, tab)


    if (hasattr(data_object,'kind') and data_object.kind == "see"):
        return s
#        print data_object
#        s = "**See also:**\n\n" + s


    if (isinstance(data_object,unicode)):
        s = data_object
        s = re.sub("([a-zA-Z0-9_]+)\(\)",":c:func:`\g<1>`",s)
        return s

    if isinstance(data_object, docParamListItemSub):
        return render_param(data_object, tab)
        
    if (hasattr(data_object, 'para')):
        s += ''.join([render_content(x, tab) for x in data_object.para])

    if isinstance(data_object, enumvalueTypeSub):
        data_object.content_ = \
           [x for x in data_object.content_ if not check_for_linked(x)]

    if (hasattr(data_object, 'content')):
        s += ''.join([render_content(x, tab) for x in data_object.content])
    elif (hasattr(data_object, 'content_')):
        s += ''.join([render_content(x, tab) for x in data_object.content_])

    if (hasattr(data_object, 'verbatim')):
        s += ''.join([render_content(x, tab) for x in data_object.verbatim])


    if (hasattr(data_object, 'parameterlist')):
        s += '\n\n' + ''.join([render_content(x, tab) for x in data_object.parameterlist])

    if (hasattr(data_object, 'parameteritem')):
        s += ''.join([render_content(x, tab) for x in data_object.parameteritem])

    if (hasattr(data_object, 'parametername')):
        s += ''.join([render_content(x, tab) for x in data_object.parametername])



    if (hasattr(data_object, 'simplesects')):
        s += ''.join([render_content(x, tab) for x in data_object.simplesects])




    if (hasattr(data_object, 'memberdef')):
        s += ''.join([render_content(x, tab) for x in data_object.memberdef])


    if (isinstance(data_object, docParaTypeSub)):
        s += '\n\n'


    if (hasattr(data_object, 'enumvalue')) and data_object.enumvalue != []:
        s += "\n**Enum Values:**\n\n" + add_indent(''.join([render_content(x, tab) for x in data_object.enumvalue]))

    if isinstance(data_object, docVerbatimTextTypeSub):
        s = s.replace("\n *","\n ")
        s = " ::\n" + add_indent(s+"\n") + "\n"

    if isinstance(data_object, enumvalueTypeSub):
        s = "\n.. c:member:: "+data_object.name+"\n" + add_indent(s)

    if hasattr(data_object, 'kind'):
        if data_object.kind == "function":

            args = data_object.argsstring.replace("&amp","&")
            args = data_object.argsstring.replace("?"," ?")
            args = re.sub("REFERENCE_PARAM\(\s*([^,]*)\s*,\s*([^\)]*)\s*\)",
                               "\g<1> &\g<2>",
                               args)
            s = ".. c:function:: " + data_object.definition + args + "\n" + add_indent(s)
            print "Rendering Doxygen function " + data_object.definition
        elif data_object.kind == "typedef":
            s = ".. c:type:: " + data_object.name + "\n" + add_indent(s)
            print "Rendering Doxygen type " + data_object.name
        elif data_object.kind == "enum":
            s = ".. c:type:: " + data_object.name + "\n" + add_indent(s)
            print "Rendering Doxygen enum " + data_object.name
        elif data_object.kind == "define":
            s = ".. c:macro:: " + data_object.name + "\n" + add_indent(s)
            print "Rendering Doxygen define " + data_object.name
        elif data_object.kind == "variable":
#            print data_object
 #           print dir(data_object)
 #           print data_object.type_
#            print dir(data_object.type_)
#            print dir(data_object.type_.content_[0])
#            print data_object.type_.content_[0].getValue()
            type_string = render_content(data_object.type_, tab)
            s = ".. c:member:: " + type_string + " " + data_object.name + "\n" + add_indent(s)
        elif data_object.kind == "return":
            s = ":return: " + s
        else:
            #print "Unknown:" + data_object.kind + "\n"             
            pass
        

    s = s.replace("___port___port___","port:")

    if s.find('__multret__') != -1:
        mult_ret_subs = [ ('{','obrace'),
                          ('}','cbrace'),
                          (' ','space'),
                          (',','comma'),
                          ('/*','ocomment'),
                          ('*/','ccomment')]
        s = s.replace('__multret__','')
        for repl, pattern in mult_ret_subs:
            s = s.replace(pattern, repl)




    return s

def render_compoundtype(type_data_object, data_object, state, content, content_offset):

    s = ".. c:type:: %s\n" % (type_data_object.name)

    print "Rendering Doxygen struct " + type_data_object.name

    compound = data_object.get_compounddef()

    if (hasattr(compound, 'briefdescription')):
        s += add_indent(render_content(compound.briefdescription,''));

    s += add_indent(render_content(compound.detaileddescription,''));

    for sectiondef in compound.sectiondef:
        if sectiondef.kind == "public-attrib":
            s += add_indent("**Structure Members:**\n\n")
            s += add_indent(render_content(sectiondef,''))


    content.data = s.split("\n")

#    print str.join("\n",content.data)


    term = nodes.Element()
    state.nested_parse(content, content_offset,term)
    
    return term.children

def render(data_object, state, content, content_offset):


    content.data = render_content(data_object,'').split("\n")


    term = nodes.Element()
    state.nested_parse(content, content_offset,term)

    return term.children

