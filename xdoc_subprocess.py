## Annoying OS incompatability, not sure why this is needed
import re
import platform
import subprocess

ostype = platform.system()

if not re.match('.*Darwin.*',ostype) and re.match('.*[W|w]in.*',ostype):
    concat_args = True
else:
    concat_args = False

use_shell = True

def Popen(*args, **kwargs):    
    kwargs['shell'] = use_shell
    if concat_args:
        args = (' '.join(args[0]),) + args[1:]
    return subprocess.Popen(*args,**kwargs)

def call(*args, **kwargs):
    kwargs['shell'] = use_shell
    if concat_args:
        args = (' '.join(args[0]),) + args[1:]
    return subprocess.call(*args,**kwargs)
