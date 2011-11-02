from docutils import nodes
from sphinx import addnodes
import sys
import re

def do_reduce(stack):
    n = stack.pop()
    if isinstance(n,nodes.emphasis) and \
       isinstance(stack[-1],nodes.literal):
        xs = stack[-1].children
        stack[-1] = addnodes.literal_emphasis()
        for x in xs + n.children:
            stack[-1] += x
    else:
        stack[-1] += n

def match(x,typ):
    if isinstance(x,typ):
        return True
    if typ == nodes.literal and isinstance(x,addnodes.literal_emphasis):
        return True
    return False

def miniparse(text):
    stack = [nodes.inline(),nodes.Text('')]
    ret = nodes.inline()
    text = text.replace('~~','\2')
    text = text.replace('**','\3')
    constructs = {'\1':nodes.inline,
                  '\2':nodes.literal,
                  '\3':nodes.strong,
                  '*':nodes.emphasis}
    for i in text:
        if i in ['*','\1','\2','\3']:
            txt = stack.pop()
            if txt.astext() != '':
                stack[-1] += txt
            if match(stack[-1],constructs[i]):
                #reduce
                do_reduce(stack)
            else:
                n = constructs[i]()
                stack.append(n)
            stack.append(nodes.Text(''))
        else:
            if stack != [] and isinstance(stack[-1],nodes.Text):
                stack[-1] = nodes.Text(stack[-1].astext() + i)
            else:
                stack.append(nodes.Text(i))

    txt = stack.pop()
    if txt.astext() != '':
        stack[-1] += txt
    while len(stack) > 1:
        do_reduce(stack)


    return stack[0]
