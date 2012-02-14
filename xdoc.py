#!/usr/bin/python
import sys
import os
import re
import sphinx
import shutil
import subprocess
from xsphinx.check_toc import checktoc
from xsphinx.run_latex import runlatex
from xsphinx.sphinx_filter import XSphinxFilter
import zipfile

# This script is slighty odd in that it is a port of a system that was based on
# Makefiles. This means that some values are passed around in the OS environment
# (ugh)

xmossphinx = None

config_defaults = {'OTHER_DOC_DIRS':[],
                   'DOXYGEN_DIRS':[],
                   'SOURCE_INCLUDE_DIRS':[],
                   'SPHINX_MASTER_DOC':'index'}

def get_config(path):
    config = {}
    f = open(os.path.join(path,'Makefile'))
    lines = f.readlines()
    f.close()
    for line in lines:
        m = re.match('(.*)=(.*)',line)
        if m:
            key = m.groups(0)[0].strip()
            value = m.groups(0)[1].strip()
            if key in config_defaults and config_defaults[key] == []:
                value = [x for x in value.split(' ') if x != '']
            config[key] = value

    if not 'SPHINX_MASTER_DOC' in config:
        rstfiles = [f for f in os.listdir(path) if re.match('.*\.rst$',f)]
        if 'index.rst' in rstfiles:
            config['SPHINX_MASTER_DOC'] = 'index'
        elif len(rstfiles) == 1:
            config['SPHINX_MASTER_DOC'] = rstfiles[0][:-4]
        else:
            sys.stderr.write("Cannot determine main rst file")

    for key,default_value in config_defaults.items():
        if not key in config:
            config[key] = default_value

    config['XDOC_DIR'] = os.path.dirname(os.path.abspath(__file__))
    config['DOC_DIR'] = os.path.abspath(path)


    for key,value in config.items():
        try:
            os.environ[key] = value
        except TypeError:
            os.environ[key] = ' '.join(value)

    return config

def rsync_dir(d,destroot):
    print "Copying %s" % d
    exclude_pattern = r'.*\.sources.*|.*\.git.*|.*\.zip|.*\.xe'
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

    cmd = 'doxygen'

    process = subprocess.Popen(cmd,cwd=doc_dir,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)

    while True:
        line = process.stdout.readline()
        if line == '':
            break
        if not re.match('.*REFERENCE.*',line):
            print line

    os.remove(doxyfile_path)

def doLatex(doc_dir,build_dir,config, master, xmoslatex=False):

    texfile = os.path.join(doc_dir,master+".tex")
    shutil.copy(os.path.join(build_dir,master+".tex"),texfile)
    os.environ['TEXINPUTS'] += build_dir + ":"
    filt = XSphinxFilter(sys.stdout, sys.stderr, os.path.join(build_dir,'latex.output'))
    texfile = master+'.tex'
    if xmoslatex:
        import_xmos(config)
        from xmossphinx.xmos_latex import make_xmos_latex
        texfile = make_xmos_latex(texfile, config)

    lines = runlatex(doc_dir,['-shell-escape','-interaction','nonstopmode',
                              texfile])

    outfile = texfile.replace('.tex','.pdf')
    if xmoslatex:
        shutil.copy(os.path.join(doc_dir,outfile),
                    os.path.join(doc_dir,master+'.pdf'))
        os.remove(texfile)

    for line in lines:
        filt.write(line)
    filt.finish()

def find_files(path):
    fs = []
    for root, dirs, files in os.walk(path):
        for f in files:
            fs.append(os.path.relpath(os.path.join(root, f),path))

    return fs

def copy_dir_to_zip(z, path, arcpath, pattern=None, exclude = None):
    for f in find_files(path):
        fpath = os.path.join(path, f)
        if (not pattern or re.match(pattern, f)) and \
                (not exclude or not f == exclude):
            z.write(fpath,arcname = os.path.join(arcpath, f))

def make_zip(path, config):
    z = zipfile.ZipFile("issue.zip","w")
    pdfpath = os.path.join(path,config['SPHINX_MASTER_DOC']+'.pdf')
    z.write(pdfpath,arcname="output.pdf")
    z.write(os.path.join(path,'seealso.xml'))
    master_html = config['SPHINX_MASTER_DOC']+'.html'
    z.write(os.path.join(path,'_build','xdehtml',master_html),
                         arcname=os.path.join('html','index.html'))
    copy_dir_to_zip(z,os.path.join(path,'_build','xdehtml'),'html',
                    pattern='.*\.html$', exclude = master_html)
    copy_dir_to_zip(z,os.path.join(path,'_build','xdehtml','_static'),
                    os.path.join('html','_static'))
    copy_dir_to_zip(z,os.path.join(path,'_build','xdehtml','images'),
                    os.path.join('html','images'))
    z.close()

def prebuild(path, xmos_prebuild=False,xmos_publish=False,docnum=None):
    global xmossphinx
    config = get_config(path)
    rsync_dirs(config['OTHER_DOC_DIRS'],'.linked_dirs')
    rsync_dirs(config['DOXYGEN_DIRS'],'.doxygen')
    rsync_dirs(config['SOURCE_INCLUDE_DIRS'],'.sources')

    sys.path.append(os.path.join(config['XDOC_DIR'],'xsphinx'))

    if xmos_prebuild:
        import_xmos(config)
        from xmossphinx.xmos_process_toc import process_toc
        from xmossphinx.check_docinfo import check_doc
        _,docnum = check_doc(path,
                             config['SPHINX_MASTER_DOC'],
                             try_to_create=xmos_publish)

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
        import xmossphinx


def build(path, config, target = 'html',subdoc=None):
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
    else:
        sys.stderr.write("xdoc: Unknown target %s\n"%target)
        exit(1)

    toc = checktoc(config['SPHINX_MASTER_DOC']+".rst",
                   config['OTHER_DOC_DIRS'],
                   path=path)
    if toc == []:
        os.environ['XMOSCOMPACTPDF']='1'
    else:
        os.environ['XMOSMANUALPDF']='1'

    config['TOC'] = toc

    os.environ['COLLECTION'] = ' '.join([x + '__0' for x in toc])

    os.environ['TEXINPUTS'] = os.path.join(config['XDOC_DIR'],'..','infr_docs','base')+":"
    os.environ['TEXINPUTS'] += os.path.join(config['XDOC_DIR'],'texinput')+":"


    os.environ['CURRENT_BUILDER'] = builder

    if subdoc:
        os.environ['_SPHINX_MASTER_DOC'] = subdoc
        os.environ['COLLECTION'] = ''
    else:
        os.environ['_SPHINX_MASTER_DOC'] = config['SPHINX_MASTER_DOC']

    build_dir = os.path.join(path,"_build",builder)
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)

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


def main(target,path='.'):
    print "Building documentation target: %s" % target
    if target in ['issue','draft']:
        config = prebuild(path,xmos_prebuild=True, xmos_publish=True)
        build(path,config,target='xref')
        for x in config['TOC']:
            build(path,config,target='xref',subdoc=x)
        build(path,config,target='xdehtml')
        build(path,config,target='xmospdf')
    else:
        config = prebuild(path,xmos_prebuild=(target in xmos_targets))
        build(path,config,target=target)

    if target in ['issue','draft','pubdraft','pubissue']:
        make_zip(path, config)

    if target in ['issue','draft']:
        from xmossphinx.upload_issue import upload
        upload(path,is_draft=(target==['draft']))

if __name__ == "__main__":
    target = sys.argv[1]
    main(target)
