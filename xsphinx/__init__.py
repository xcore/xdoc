from docutils import nodes

def miniparse(text):

    stack = ['\1']
    content = ""
    ret = []
    text = text.replace('~~','\2')
    text = text.replace('**','\3')
    constructs = {'\1':nodes.term,
                  '\2':nodes.literal,
                  '\3':nodes.strong,
                  '*':nodes.emphasis}
    for i in text:
        if i in ['*','\1','\2','\3']:
            prev = stack[-1]
            n = constructs[prev]()
            n += nodes.Text(content)
            ret.append(n)
            content = ""
            if i == prev:
                stack.pop()
            else:
                stack.append(i)
        else:
            content += i

    if content != '':
        n = constructs[stack.pop()]()
        n += nodes.Text(content)
        ret.append(n)
    return ret
