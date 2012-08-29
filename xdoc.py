#!/usr/bin/python
import sys
import os
import re
import sphinx
import shutil
import subprocess
import platform
from xsphinx.check_toc import checktoc
from xsphinx.run_latex import runlatex
from xsphinx.sphinx_filter import XSphinxFilter
import zipfile
import copy
# This script is slighty odd in that it is a port of a system that was based on
# Makefiles. This means that some values are passed around in the OS environment
# (ugh)

xmossphinx = None

config_defaults = {'OTHER_DOC_DIRS':[],
                   'DOXYGEN_DIRS':[],
                   'SOURCE_INCLUDE_DIRS':[],
                   'SPHINX_MASTER_DOC':'index'}

def get_master_doc(path):
    rstfiles = [f for f in os.listdir(path) if re.match('.*\.rst$',f)]
    if 'index.rst' in rstfiles:
        return 'index'
    elif len(rstfiles) == 1:
        return rstfiles[0][:-4]
    else:
        sys.stderr.write("Cannot determine main rst file")

def get_title(path):
    toc,title = checktoc(os.path.join(path,get_master_doc(path)+'.rst'))
    return title


def expand(s, config):
    for key, value in config.items():
        if type(value) == list:
            continue
        s = s.replace("$(%s)"%key, value)
        s = s.replace("$%s"%key, value)
    return s

def get_config(path,config={}):
    config = copy.copy(config)
    if os.path.exists(os.path.join(path,'Makefile')):
        f = open(os.path.join(path,'Makefile'))
        lines = f.readlines()
        f.close()
    else:
        lines = ''
    prev = None
    for line in lines:
        if prev:
            line = prev + line
            prev = None
        if len(line)>1 and line[-2] == '\\':
            prev = line[:-2]
            continue
        line = expand(line, config)
        m = re.match('([^\+]*)(\+?)=(.*)',line)
        if m:
            key = m.groups(0)[0].strip()
            plus = m.groups(0)[1].strip()
            value = m.groups(0)[2].strip()
            is_list = key in config_defaults and config_defaults[key] == []

            if is_list:
                value = [x for x in value.split(' ') if x != '']

            if is_list and plus=='+' and key in config:
                config[key] += value
            else:
                config[key] = value

    if not 'SPHINX_MASTER_DOC' in config:
        config['SPHINX_MASTER_DOC'] = get_master_doc(path)


    for key,default_value in config_defaults.items():
        if not key in config:
            config[key] = copy.copy(default_value)


    if hasattr(sys,'_MEIPASS'):
        config['XDOC_DIR'] = sys._MEIPASS
    elif '_MEIPASS2' in os.environ:
        config['XDOC_DIR'] = os.environ['_MEIPASS2']
    else:
        config['XDOC_DIR'] = os.path.dirname(os.path.abspath(__file__))

    config['DOC_DIR'] = os.path.abspath(path)


    for key,value in config.items():
        try:
            os.environ[key] = value
        except TypeError:
            os.environ[key] = ' '.join(value)

    for key,value in config.items():
        try:
            if '..' in value:
                #print value
                value = [x for x in value if x != '..']
                for d in os.listdir('..'):
                    if os.path.isdir(os.path.join('..',d)) and \
                            not d == os.path.basename(os.path.abspath('.')):
                        value.append(os.path.join('..',d))

                config[key] = value
        except:
            pass

    return config

def rsync_dir(d,destroot):
    print "Copying %s" % d
    exclude_pattern = r'.*\.sources.*|.*\.git.*|.*\.zip|.*\.xe|.*\.linked_dirs.*|.*\.doxygen.*|.*\.support.*'
    for root, dirs, files in os.walk(d):
        for f in files:
            src = os.path.join(root, f)
            dst = os.path.normpath(os.path.join(destroot, os.path.relpath(root,d), f))
            dstpath = os.path.dirname(dst)
            if not re.match(exclude_pattern, src):
                copyfile = True
                if not os.path.exists(dstpath):
                    os.makedirs(os.path.dirname(dst))
                if os.path.exists(dst):
                    dst_mod_time = os.stat(dst).st_mtime
                    src_mod_time = os.stat(src).st_mtime
                    if src_mod_time - dst_mod_time < 1:
                        copyfile = False
                if copyfile:
                    pass
                    shutil.copy2(src, dst)




def rsync_dirs(dirlist, dest):
    for d in dirlist:
            rsync_dir(d,os.path.join(dest,os.path.basename(d)))


def doDoxygen(xdoc_dir, doc_dir):
    print "Running Doxygen"
    build_path = os.path.join(doc_dir,'_build','doxygen')
    doxyfile_path = os.path.join(doc_dir, 'Doxyfile')
    if not os.path.exists(build_path):
        os.makedirs(build_path)

    shutil.copy(os.path.join(xdoc_dir, 'xsphinx', 'Doxyfile'),
                doxyfile_path)

    f = open(doxyfile_path,"a");
    if hasattr(sys,'_MEIPASS'):
        print "Using xdoxygen"
        cmd = 'xdoxygen'
        f.write('\nINPUT_FILTER = xdoxygen_prefilter\n')
    else:
        cmd = 'doxygen'
        f.write('\nINPUT_FILTER           = "python $(XDOC_DIR)/xsphinx/xc_prefilter.py\n"')

    process = subprocess.Popen(cmd,cwd=doc_dir,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)

    while True:
        line = process.stdout.readline()
        if line == '':
            break
        if not re.match('.*REFERENCE.*',line):
            print line

    process.wait()
    os.remove(doxyfile_path)

ostype = platform.system()

if not re.match('.*Darwin.*',ostype) and re.match('.*[W|w]in.*',ostype):
    listsep = ';'
else:
    listsep = ':'

def doLatex(doc_dir,build_dir,config, master, xmoslatex=False):
    if hasattr(sys,'_MEIPASS'):
        os.environ['TEXINPUTS'] = os.path.join(sys._MEIPASS,'infr_docs','base')+listsep + os.path.join(sys._MEIPASS,'texinputs')+listsep
    else:
        os.environ['TEXINPUTS'] = os.path.join(config['XDOC_DIR'],'..','infr_docs','base')+listsep + os.path.join(config['XDOC_DIR'],'..','..','infr_docs','base')+listsep
    os.environ['TEXINPUTS'] += os.path.join(config['XDOC_DIR'],'texinput')+listsep
    texfile = os.path.join(doc_dir,master+".tex")
    if not os.path.exists(os.path.join(build_dir,master+".tex")):
        print "Cannot find latex file. Something must have gone wrong"
        exit(1)

    #shutil.copy(os.path.join(build_dir,master+".tex"),texfile)
    os.environ['TEXINPUTS'] += os.path.abspath(build_dir) + listsep + os.path.abspath(doc_dir) + listsep
    filt = XSphinxFilter(sys.stdout, sys.stderr, os.path.join(build_dir,'latex.output'))
    texfile = master+'.tex'
    if xmoslatex:
        import_xmos(config)
        from xmossphinx.xmos_latex import make_xmos_latex
        texfile = make_xmos_latex(build_dir, texfile, config)

    lines = runlatex(build_dir,['-shell-escape','-interaction=nonstopmode',
                              texfile])

    outfile = texfile.replace('.tex','.pdf')
    if xmoslatex:
        shutil.copy(os.path.join(build_dir,outfile),
                    os.path.join(build_dir,master+'.pdf'))
        os.remove(os.path.join(build_dir,outfile))

    for line in lines:
        filt.write(line)

    sys.stdout, sys.stderr = filt.finish()

def find_files(path):
    fs = []
    for root, dirs, files in os.walk(path):
        for f in files:
            fs.append(os.path.relpath(os.path.join(root, f),path))

    return fs


def write_html_to_zip(z, fpath, arcpath):
    html_file = open(fpath)
    html_str = html_file.read()
    html_file.close()
    html_str = html_str.replace('_images','images')
    html_str = html_str.replace('_static/images','images')
    z.writestr(arcpath, html_str)


def copy_dir_to_zip(z, path, arcpath, pattern=None, exclude = None):
    for f in find_files(path):
        fpath = os.path.join(path, f)
        if (not pattern or re.match(pattern, f)) and \
                (not exclude or not f == exclude):
            if re.match('.*\.html$',f):
                write_html_to_zip(z, fpath, os.path.join(arcpath, f))
            else:
                z.write(fpath,arcname = os.path.join(arcpath, f))

def make_zip(path, config):
    z = zipfile.ZipFile("issue.zip","w")
    pdfpath = os.path.join(path,'_build','xlatex',config['SPHINX_MASTER_DOC']+'.pdf')
    z.write(pdfpath,arcname="output.pdf")
    z.write(os.path.join(path,'_build','seealso.xml'),arcname='seealso.xml')
    master_html = config['SPHINX_MASTER_DOC']+'.html'
    write_html_to_zip(z,
                      os.path.join(path,'_build','xdehtml',master_html),
                      os.path.join('html','index.html'))
    copy_dir_to_zip(z,os.path.join(path,'_build','xdehtml'),'html',
                    pattern='.*\.html$', exclude = master_html)
    copy_dir_to_zip(z,os.path.join(path,'_build','xdehtml','_static'),
                    os.path.join('html','_static'))
    copy_dir_to_zip(z,os.path.join(path,'_build','xdehtml','_static','images'),
                    os.path.join('html','images'))
    copy_dir_to_zip(z,os.path.join(path,'_build','xdehtml','_images'),
                    os.path.join('html','images'))
    z.close()

def prebuild(path, config={},xmos_prebuild=False,xmos_publish=False,docnum=None):
    global xmossphinx
    config = get_config(path,config)
    rsync_dirs(config['OTHER_DOC_DIRS'],os.path.join('_build','.linked_dirs'))
    rsync_dirs(config['DOXYGEN_DIRS'],os.path.join('_build','.doxygen'))
    rsync_dirs(config['SOURCE_INCLUDE_DIRS'],os.path.join('_build','.sources'))

    sys.path.append(os.path.join(config['XDOC_DIR'],'xsphinx'))

    if xmos_prebuild:
        import_xmos(config)
        from xmossphinx.xmos_process_toc import process_toc
        from xmossphinx.check_docinfo import check_doc

        auto_create = 'AUTO_CREATE' in config and config['AUTO_CREATE']=='1'
        if 'ALT_TITLE' in config:
            alt_title = config['ALT_TITLE']
        else:
            alt_title = None

        _,docnum = check_doc(path,
                             config['SPHINX_MASTER_DOC'],
                             try_to_create=xmos_publish,
                             auto_create=auto_create,
                             alt_title = alt_title)

        print "Processing document structure for xref database"
        process_toc(os.path.join(path,config['SPHINX_MASTER_DOC']+".rst"),
                    docnum,
                    config['OTHER_DOC_DIRS'])
        if docnum:
            config['DOCNUM'] = docnum
            os.environ['DOCNUM'] = docnum

    if config['DOXYGEN_DIRS'] != []:
        doDoxygen(config['XDOC_DIR'], config['DOC_DIR'])


    return config

def import_xmos(config):
    global xmossphinx
    if not xmossphinx:
        sys.path.append(os.path.join(config['XDOC_DIR'],'..','infr_docs'))
        sys.path.append(os.path.join(config['XDOC_DIR'],'..','infr_docs','xmossphinx'))
        sys.path.append(os.path.join(config['XDOC_DIR'],'..','infr_docs','tool_xpd'))
        import xmossphinx

def pop_if_exists(d, val):
    if val in d:
        d.pop(val)

def build(path, config, target = 'html',subdoc=None):
    pop_if_exists(os.environ,'XMOSLATEX')
    if target == 'html':
        builder = 'html'
    elif target == 'gh-pages':
        builder = 'html'
    elif target == 'pdf':
        builder = 'xlatex'
    elif target == 'xmospdf':
        builder = 'xlatex'
        os.environ['XMOSLATEX'] = '1'
    elif target == 'xref':
        builder = 'xmos_xref'
        os.environ['XMOSLATEX'] = '1'
    elif target == 'xmoshtml':
        builder = 'xdehtml'
        os.environ['USE_XDEONLY_HTML'] = "0"
    elif target == 'xdehtml':
        builder = 'xdehtml'
        os.environ['USE_XDEONLY_HTML'] = "1"
    elif target == 'xdetutorial':
        builder = 'xdehtml'
        os.environ['USE_XDEONLY_HTML'] = "1"
        os.environ['XDETUTORIAL_HTML'] = "1"
    elif target == 'text':
        builder = 'text'
    else:
        sys.stderr.write("xdoc: Unknown target %s\n"%target)
        exit(1)

    toc,title = checktoc(config['SPHINX_MASTER_DOC']+".rst",
                         config['OTHER_DOC_DIRS'],
                         path=path)

    if toc == []:
        os.environ['XMOSCOMPACTPDF']='1'
        os.environ['XMOSMANUALPDF']='0'
    else:
        os.environ['XMOSCOMPACTPDF']='0'
        os.environ['XMOSMANUALPDF']='1'

    os.environ['SPHINX_PROJECT_NAME'] = title

    config['TOC'] = toc

    os.environ['COLLECTION'] = ' '.join([x + '__0' for x in toc])



    os.environ['CURRENT_BUILDER'] = builder

    os.environ['OTHER_DOC_DIRS_ABS'] = ' '.join([os.path.abspath(x) for x in config['OTHER_DOC_DIRS']])

    if subdoc:
        os.environ['_SPHINX_MASTER_DOC'] = subdoc
        os.environ['COLLECTION'] = ''
    else:
        os.environ['_SPHINX_MASTER_DOC'] = config['SPHINX_MASTER_DOC']

    build_dir = os.path.join(path,"_build",builder)
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)


    if 'XDEHTML_UNPAGED_OUTPUT' in config:
        os.environ['XDEHTML_UNPAGED_OUTPUT'] = config['XDEHTML_UNPAGED_OUTPUT']
    else:
        os.environ['XDEHTML_UNPAGED_OUTPUT'] = '0'

    if 'SOURCE_SUFFIX' in config:
        os.environ['SOURCE_SUFFIX'] = config['SOURCE_SUFFIX']
    else:
        os.environ['SOURCE_SUFFIX'] = '.rst'

    os.makedirs(build_dir)

    if target == 'xref':
        print "Getting xref info"
    else:
        print "Running Sphinx"

    filt = XSphinxFilter(sys.stdout, sys.stderr, os.path.join(build_dir,'sphinx.output'))
    sys.stdout = filt
    sys.stderr = filt

    sphinx.main(['sphinx-build',
                 '-c',os.path.join(config['XDOC_DIR'],'xsphinx'),
                 '-b',builder,
                 path,
                 os.path.join(path,"_build",builder)])
    sys.stdout, sys.stderr = filt.finish()

    if builder == 'xlatex':
        doLatex(path,
                os.path.join(path,"_build",builder),
                config,
                config['SPHINX_MASTER_DOC'],
                xmoslatex = target in xmos_targets)

    if target != 'xref':
        print "Build Complete"

xmos_targets = ['xmoshtml','xdehtml','xmospdf','issue','draft','xref']

class StdInChecker(object):
    """ This class is to try and debug a strange occurrence where sys.stdin
        gets closed somewhere. Putting this class in actually stopped it
        happening so I'm going to leave it here whilst it is under
        investigation.
    """
    def __init__(self, f):
        self.f = f

    def read(self):
        return self.f.read()

    def readline(self):
        return self.f.readline()

    def close(self):
        raise BaseException

def main(target,path='.',config={}):
    sys.stdin = StdInChecker(sys.stdin)
    print "Building documentation target: %s" % target
    curdir = os.path.abspath(os.curdir)
    os.chdir(path)
    path = '.'
    if target == 'swlinks':
        config = get_config(path,config)
        import_xmos(config)
        from xmossphinx.xmos_check_swlinks import check_swlinks
        check_swlinks(path)
    elif target == 'update_sw':
        config = get_config(path,config)
        import_xmos(config)
        from xmossphinx.xmos_check_swlinks import update_sw
        update_sw(path)
    elif target in ['issue','draft']:
        config = prebuild(path,config,xmos_prebuild=True, xmos_publish=True)
        build(path,config,target='xref')
        for x in config['TOC']:
            build(path,config,target='xref',subdoc=x)
        build(path,config,target='xdehtml')
        build(path,config,target='xmospdf')
    elif target == 'justlatex':
        config = prebuild(path,config,xmos_prebuild=True)
        doLatex(path,
                os.path.join(path,"_build",'xlatex'),
                config,
                config['SPHINX_MASTER_DOC'],
                xmoslatex = True)
    else:
        config = prebuild(path,config,xmos_prebuild=(target in xmos_targets))
        build(path,config,target=target)

    if target in ['issue','draft','pubdraft','pubissue']:
        make_zip(path, config)

    if target in ['issue','draft']:
        from xmossphinx.upload_issue import upload
        force_upload = 'FORCE_UPLOAD' in config and config['FORCE_UPLOAD']=='1'
        title = get_title(path)
        upload(path,is_draft=(target=='draft'),force_upload=force_upload,
               upload_title = "Document: %s" % title)

    os.chdir(curdir)



if __name__ == "__main__":
    target = sys.argv[1]
    main(target)
