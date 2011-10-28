% XMOS Modern LaTeX class file
% Author: Douglas Watt
% Last Modified: 11/12/10

\NeedsTeXFormat{LaTeX2e}[1995/12/01]
\ProvidesClass{xcore}
              [2010/12/10 v2.0b XCore Style Class]

% Command line options from Makefile
\ifcsname ifinternal\endcsname\else 
  \expandafter\let\csname ifinternal\expandafter\endcsname 
                  \csname iffalse\endcsname 
\fi 
			  
% Class Options (default to Article, no other options)
\newif\ifonline\onlinetrue
\newif\ifprintedbook\printedbookfalse
\newif\ifonlinebook\onlinebookfalse
\newif\ifnochapters\nochaptersfalse
\newif\ifnodms\nodmsfalse

% Default to article
\newif\ifarticle\articletrue
\DeclareOption{article}{\articletrue}
\newif\ifmanual\manualfalse
\DeclareOption{manual}{\manualtrue\articlefalse}
\newif\ifbook\bookfalse
\DeclareOption{book}{\booktrue\printedbooktrue\onlinebookfalse\articlefalse\onlinefalse}
\DeclareOption{ebook}{\booktrue\printedbookfalse\onlinebooktrue\articlefalse\onlinetrue}
\newif\ifdatasheet\datasheetfalse
\DeclareOption{datasheet}{\datasheettrue\manualtrue\articlefalse\nochapterstrue}
\newif\ifarow\arowfalse
\DeclareOption{arow}{\arowtrue\onlinefalse}
\newif\ifcameraready\camerareadyfalse
\DeclareOption{a4camera}{\camerareadytrue\onlinefalse}
\newif\ifconfidential\confidentialfalse
%Internal files always confidential
\ifinternal\confidentialtrue\fi
\DeclareOption{confidential}{\confidentialtrue}
\newif\ifsafefont\safefontfalse
\DeclareOption{draftfont}{\safefonttrue\PassOptionsToClass{draft}{memoir}}
\DeclareOption{draft}{\PassOptionsToClass{draft}{memoir}}
\DeclareOption*{\ClassError{xmosmodern}{The `\CurrentOption' option is not supported}}
\DeclareOption{nochapters}{\nochapterstrue}
\DeclareOption{nodms}{\nodmstrue}
\DeclareOption{linux}{\linuxtrue}
\newif\ifasian\asianfalse
\newif\ifen\entrue
\DeclareOption{en}{\entrue}
\newif\ifjp\jpfalse
\DeclareOption{jp}{\jptrue\enfalse\pdflatexfalse\asiantrue}
\newif\iftw\twfalse
\DeclareOption{tw}{\twtrue\enfalse\pdflatexfalse\asiantrue}
\newif\ifzh\zhfalse
\DeclareOption{zh}{\zhtrue\enfalse\pdflatexfalse\asiantrue}
\newif\ifkr\krfalse
\DeclareOption{kr}{\krtrue\enfalse\pdflatexfalse\asiantrue}
\ProcessOptions

% Determine which class and options to load
\ifprintedbook
\LoadClass[twoside,openright,onecolumn,10pt,showtrims]{memoir}
\ifcameraready\else\showtrimsoff\fi
\else\ifmanual
\LoadClass[oneside,onecolumn,article,9pt]{memoir}
\else
\LoadClass[oneside,onecolumn,article,10pt]{memoir}
\fi\fi

% Both online and offline books should use the same value for \chaptername
\ifonlinebook
\renewcommand{\chaptername}{\Sec}
\fi

\RequirePackage{ifpdf}

% PDF Properties
\ifpdf
\pdfminorversion=5
\pdfobjcompresslevel=3
\pdfcompresslevel=9
\fi

% Needed for internal calculations
\RequirePackage{calc}

% Set the paper stock size
\ifcameraready
\setstocksize{297mm}{210mm}
\else\ifarow
\setstocksize{297mm}{210mm}
\else
\setstocksize{235mm}{178mm}
\fi\fi

% Set the trimmed size
\settrimmedsize{235mm}{178mm}{*}
\setlength{\trimtop}{0pt}
\setlength{\trimedge}{\stockwidth}
\addtolength{\trimedge}{-\paperwidth}

% Title Width
\newlength{\titlewidth}
\setlength{\titlewidth}{135mm}

% Set the type block size
\newlength{\typeblockwidth}
\ifmanual
\setlength{\typeblockwidth}{120mm}
\settypeblocksize{185mm}{\typeblockwidth}{*}
\else
\setlength{\typeblockwidth}{135mm}
\settypeblocksize{44\onelineskip}{\typeblockwidth}{*}
\fi

\ifprintedbook
\setlrmargins{0.8in}{*}{*}
\setmarginnotes{0.2cm}{0.8cm}{\onelineskip}
\else\ifmanual
% Note: right margin comes first due to swap below
\ifonline\setlrmargins{40mm}{*}{*}\else\setlrmargins{18mm}{*}{*}\fi
\setmarginnotes{4mm}{18mm}{\onelineskip}
\setsecindent{-22mm}
\else
\setlrmargins{*}{*}{1.0}
\fi\fi

% Fullwidth environment, temporarily change margins in manual

\def\@infullwidth{0}
\newlength{\textfullwidth}
\setlength{\textfullwidth}{\textwidth}
\ifmanual
% Adjustments not quite right apparently, re-adjust based on pdflatex warning msg
\newenvironment{fullwidth}{\addtolength{\textfullwidth}{22mm-0.43306pt}\begin{adjustwidth}{-22mm}{}\setlength\LTleft{-22mm}\def\@infullwidth{1}}{\end{adjustwidth}\addtolength{\textfullwidth}{-22mm+0.43306pt}\setlength\LTleft{0mm}\def\@infullwidth{0}}
\newlength{\absspace}
% Tex seems to get 1.43666pt out when attempt to insert image of \paperwidth
\setlength{\absspace}{(\paperwidth-\textwidth-22mm)/2}
\newenvironment{absolutefullwidth}{\begin{adjustwidth}{-\absspace-22mm}{-\absspace-1.43666pt}}{\end{adjustwidth}}
\else
\newenvironment{fullwidth}{}{}
\fi

\newcommand{\fullwidthsubsecadjust}{\setsubsecindent{-22mm}}
\newcommand{\fullwidthsubsecrevert}{\setsubsecindent{0mm}}

% Set UL margins
\setulmargins{2.5cm}{*}{*}
\setheadfoot{\onelineskip}{2\onelineskip}
\setheaderspaces{*}{2\onelineskip}{*}

% Finalise layout
\newlength{\manualadjust}
\setlength{\manualadjust}{32mm}
\ifpdf\fixpdflayout\fi
\checkandfixthelayout[lines]
\newlength{\adjustforbug}
\setlength{\adjustforbug}{-2mm}
\ifbook
  \ifarow 
    % AR requires centered on page
    \addtolength{\evensidemargin}{-16mm}
    \addtolength{\oddsidemargin}{16mm}
    \addtolength{\topmargin}{32mm+\adjustforbug}
  \fi
\else\ifmanual
  \ifcameraready
    % Need to base off the A4 dimensions (extra 32mm width)
	\setlength{\oddsidemargin}{\evensidemargin-32mm}   % right   FIX
  \else\ifarow
    % As above, but center in page
    \setlength{\oddsidemargin}{\evensidemargin-16mm}   % right
    \setlength{\evensidemargin}{\oddsidemargin}
	\addtolength{\topmargin}{32mm+\adjustforbug}
  \fi\fi
\fi\fi

% CJK 
\newcommand{\cjktext}[1]{\begin{CJK}{UTF8}{}#1\end{CJK}}

% Part Styles
\renewcommand*{\thepart}{\Alph{part}}
\renewcommand{\partnamefont}{\hspace*{-22mm}\normalfont\Huge\sffamily\raggedright}
\renewcommand{\partnumfont}{\normalfont\Huge\sffamily}
\renewcommand{\parttitlefont}{\hspace*{-22mm}\normalfont\Huge\scshape\raggedright}
\renewcommand*{\beforepartskip}{\vspace*{92pt}} % FIX: not sure why 88pt elsewhere, possibly minipage adjustment
\renewcommand*{\afterpartskip}{\hspace*{-22mm}\rule{22mm}{0.6mm}\rule{\linewidth}{0.6mm}\\[0.5cm]}

% Chapter Styles
\RequirePackage[final]{graphicx}
\newlength{\numberheight}
\newlength{\barlength}

\makechapterstyle{veeloen}{%
\setlength{\beforechapskip}{40pt}
\setlength{\midchapskip}{25pt}
\setlength{\afterchapskip}{40pt}
\renewcommand{\chapnamefont}{\sffamily\LARGE\flushright}
\renewcommand{\chapnumfont}{\sffamily\HUGE}
\renewcommand{\chaptitlefont}{\sffamily\HUGE\bfseries\flushright}
\renewcommand{\printchaptername}{\chapnamefont\MakeUppercase{\textls[500]{\@chapapp}}}
\renewcommand{\chapternamenum}{}
\ifmanual
\setlength{\numberheight}{11mm}
\else
\setlength{\numberheight}{16mm}
\fi
\setlength{\barlength}{\paperwidth}
\addtolength{\barlength}{-\textwidth}
\addtolength{\barlength}{-\spinemargin}
\renewcommand{\printchapternum}{%
\makebox[0pt][l]{%
%FIXed was .8 then shrunk margin
\hspace{.4em}%
\resizebox{!}{\numberheight}{\chapnumfont \thechapter}%
\hspace{.4em}%
\rule{\barlength}{\numberheight}}}
\makeoddfoot{plain}{}{}{\thepage}
}

\makechapterstyle{smallveelo}{%
\setlength{\afterchapskip}{40pt}
\renewcommand*{\chapterheadstart}{\vspace*{40pt}}
\renewcommand*{\afterchapternum}{\par\nobreak\vskip 25pt}
\renewcommand*{\chapnamefont}{\sffamily\LARGE\flushright}
\renewcommand*{\chapnumfont}{\sffamily\HUGE}
\renewcommand*{\chaptitlefont}{\sffamily\HUGE\bfseries\flushright}
\renewcommand*{\printchaptername}{%
\chapnamefont\MakeUppercase{\textls[500]{\@chapapp}}}
\renewcommand*{\chapternamenum}{}
\setlength{\beforechapskip}{18mm} % 18
\setlength{\midchapskip}{\paperwidth}
\addtolength{\midchapskip}{-\textwidth}
\addtolength{\midchapskip}{-\spinemargin}
\renewcommand*{\printchapternum}{%
  \makebox[0pt][l]{\hspace{.8em}%
  \resizebox{15mm}{!}{\chapnumfont \thechapter}%
  \hspace{.8em}%
  \rule{\midchapskip}{\beforechapskip}%
}}%
}

\makechapterstyle{altchapters}{%
\setlength{\afterchapskip}{\ifmanual0pt\else5\baselineskip\fi}
\setlength{\beforechapskip}{36pt}
\setlength{\midchapskip}{\textwidth}
\addtolength{\midchapskip}{-\beforechapskip}
\renewcommand*{\chapterheadstart}{\vspace*{88pt}}
\renewcommand*{\chaptitlefont}{\huge\sffamily\bfseries\raggedright}
\renewcommand*{\chapnumfont}{\chaptitlefont}
\renewcommand*{\printchaptername}{}
\renewcommand*{\chapternamenum}{}
\renewcommand*{\afterchapternum}{}
\renewcommand*{\printchapternum}{%
\ifmanual\hspace*{-22mm}\fi\begin{minipage}[t]{\beforechapskip}
{\vspace{0pt}\chapnumfont%%%\figureversion{lining}
\thechapter}
\end{minipage}}
\renewcommand*{\printchaptertitle}[1]{%
\hfill\begin{minipage}[t]{\midchapskip}
{\vspace{0pt}\ifmanual\hspace*{-22mm}\fi\chaptitlefont ##1\par}\end{minipage}}
\renewcommand*{\afterchaptertitle}{%
\par\vspace{\baselineskip}%
\ifmanual\else\rule[2mm]{\textwidth}{1.2pt}\fi \par\nobreak\noindent \vskip\afterchapskip}}

% Set chapter and section styles/number depth
\ifprintedbook
\chapterstyle{veeloen}
\else\ifarticle
\chapterstyle{article}
\renewcommand*\thesection{\arabic{section}}
\else
\chapterstyle{altchapters}
\fi\fi

% Number section depth up to X.Y.Z (for books this gives C.X.Y.Z)
\maxsecnumdepth{subsubsection}

% Disable chapters if flagged with \nochapters
\ifnochapters
\renewcommand*\thesection{\arabic{section}}
\fi

\newcommand{\MoreThanNineChapters}{\chapterstyle{smallveelo}}
\newcommand{\FourDigitsInTocSection}{\setlength{\cftsectionnumwidth}{1.1cm}}

% Footnote styles
\newfootnoteseries{P}
\renewcommand*{\@makefnmarkP}[1]{\slashfracstyle{(X #1)}}
\footmarkstyleP{#1--}

\setlength{\footmarkwidth}{1.8em}
\setlength{\footmarksep}{0em}
\footmarkstyleP{\MakeUppercase{#1}.\hfill}

% Indexing
\makeindex
\ifjp\makeindex[jp]\xindyindex\fi
\iftw\makeindex[tw]\xindyindex\fi
\ifzh\makeindex[zh]\xindyindex\fi
\iftw\makeindex[kr]\xindyindex\fi

\RequirePackage{amsmath}
\RequirePackage[cleanup={}]{pstool} % for generating custom eps to pdf graphics for datasheets, can add mode=nonstop,cleanup={} for debug (.tex, .dvi, .ps, .pdf, .log, .aux)
\ifpdf\RequirePackage[activate={true,nocompatibility},final]{microtype}\fi
\RequirePackage{stmaryrd}
\RequirePackage{alltt}
\RequirePackage{amsfonts}
\RequirePackage{setspace}
\RequirePackage{multicol}
\RequirePackage{tabularx}
\RequirePackage{ifthen}
\RequirePackage{longtable} 
%\setlength{\LTpost}{-1em}
\newcolumntype{Y}{>{\raggedright\arraybackslash}X}
\newcolumntype{y}{>{\small\raggedright\arraybackslash}X}
\RequirePackage{textcomp}
\RequirePackage{url}
\RequirePackage{listings}
\RequirePackage{gensymb}
\RequirePackage{manfnt}
\RequirePackage{pifont}
\RequirePackage{xspace}
\RequirePackage{multirow}
\RequirePackage{colortbl}
\RequirePackage{varioref}
\RequirePackage{fixltx2e}
\RequirePackage{chngcntr}
\RequirePackage{booktabs}
\RequirePackage{enumitem}
\RequirePackage{placeins} % defines \FloatBarrier command
\RequirePackage{flafter} % floats come after reference
\RequirePackage[raggedright]{ragged2e}
\RequirePackage{float}
\RequirePackage{marginnote} % works properly with \reversemarginpar to always use left margins 
\RequirePackage{layouts} % only to debug, for printing lengths
\RequirePackage{units}

% Load the required symbols
\RequirePackage{savesym}
\RequirePackage{marvosym}
\savesymbol{Cross} % conflict between marvosym and bbding
\savesymbol{checkmark} % conflict between dingbat and AMS
\RequirePackage{bbding}
\RequirePackage{dingbat}

% Localisation
\ifjp\RequirePackage{indentfirst}\fi
\iftw\RequirePackage{indentfirst}\fi
\ifzh\RequirePackage{indentfirst}\fi
\ifkr\RequirePackage{indentfirst}\fi

% PDF Settings (must load after other packages)
\ifonline
\ifasian
\RequirePackage[hyperindex=false,hyperfootnotes=false]{hyperref}
\else
\RequirePackage[hyperindex=true,hyperfootnotes=false]{hyperref}
\fi
\hypersetup{%
  %pdfkeywords        = {Event-driven processor, RELEASE:1,18mm,33mm,"Publication Date: \$DATE", RELEASE:1,XXX,YYY,"\$YEAR XMOS Ltd. All Rights Reserved.", RELEASE:L,XXX,YYY,"\$YEAR by XMOS Limited."},
  pdfcreator         = {\LaTeX},
  pdfpagemode        = UseOutlines,
  pdfdisplaydoctitle = true,
  pdfstartview       = Fit,
  baseurl            = {http://www.xmos.com/},
  pdfpagelayout      = SinglePage,
  breaklinks
}
\newcommand{\pdfMakeTitle}{\hypersetup{pdftitle={\atTheTitle}}}
\newcommand{\pdfMakeAuthor}{\hypersetup{pdfauthor={\ifx\@author\@empty XMOS Limited\else\@author\fi}}}
\RequirePackage{memhfixc}
\hypersetup{pdfproducer = {XMOS Modern LaTeX Class File (Version 2.0)}}
\hypersetup{colorlinks = true, linkcolor = blue, citecolor = blue, urlcolor = blue }
\fi

% PDF named sections
\newcommand{\pdfsection}[2]{\section[#1]{\hyperdef{sectionname}{#2}{#1}}}
\newcommand{\pdfsubsection}[2]{\subsection[#1]{\hyperdef{sectionname}{#2}{#1}}}
\newcommand{\pdfsubsectiontwo}[3]{\subsection[#1]{\hyperdef{sectionname}{#2}{#1}\hyperdef{sectionname}{#3}{}}}
\newcommand{\pdfsubsectionthree}[4]{\subsection[#1]{\hyperdef{sectionname}{#2}{#1}\hyperdef{sectionname}{#3}{}\hyperdef{sectionname}{#4}{}}}

% Title Page
%\def\and{\\[0.5em]}
\def\and{, }
\renewcommand{\title}[1]{\def\atTheTitle{#1}\def\@pdfTitle{#1}} \title{}
\ifen\else
\newcommand{\entitle}[1]{\def\atEnTitle{#1}} \entitle{}
\fi
\renewcommand{\author}[1]{\def\@author{#1}\def\theAuthor{#1}} \author{}
\newcommand{\translator}[1]{\def\atTheTranslator{#1}} \translator{}
\newcommand{\version}[1]{\def\theVersion{#1\xspace}} \version{}
\newcommand{\yearmonthday}[3]{\def\atTheYear{#1}\def\atTheDate{#1/#2/#3}} \yearmonthday{\number\year}{\number\month}{\number\day}
\newcommand{\xmospart}[1]{\def\thexmospart{#1}}
\newcommand{\auth}[2]{{#1\ }{\uppercase{#2}}}
\newcommand{\authx}[3]{{#1\ }{#2#3}} % Depricate
\newcommand{\inprint}[1]{\def\@theBookInPrint{#1}} \inprint{}
\newcommand{\inen}[1]{\def\@theBookInEN{#1}} \inen{}
\newcommand{\intw}[1]{\def\@theBookInTW{#1}} \intw{}
\newcommand{\inzh}[1]{\def\@theBookInZH{#1}} \inzh{}
\newcommand{\injp}[1]{\def\@theBookInJP{#1}} \injp{}
\newcommand{\inkr}[1]{\def\@theBookInKR{#1}} \inkr{}
\newcommand{\notes}[1]{\def\atTheNotes{#1}} \notes{}

% Start/Finish (Controls CJK/Disclaimer)
\newcommand{\AddedMyOwnDisclaimer}{\def\@disclaim{1}}

%% English
\ifen
\newcommand{\start}{\begin{document}}
\newcommand{\valuedcustomer}{\input{valued_en}}
\newcommand{\finish}{\ifdefined\@disclaim\else\makepubpage\fi\ifthenelse{\value{revcounter}=0}{}{\def\revisionerror{1}}\ifdefined\revisionerror\ClassError{xmosmodern}{The revision for the latest document is incorrect}\fi\end{document}}
\fi


% This interferes with pstool, which redefines document
\ifdefined\@notinpstool
\AtEndDocument{\ifdefined\@disclaim\else\makepubpage\fi}
\fi

% Note: This must be included after AtEndDocument
\RequirePackage{lastpage}

% Publisher Page
\newcounter{sheetsavedcounter}
\newlength{\ppagespace}
\setlength{\ppagespace}{1.5em}
\newcommand{\by}{\emph{by}}
\newcommand{\makepubpage}{
\def\@disclaim{1}
\footnotesize
\flushbottom
}

% Copyright Symbol (needed for languages without (C) symbol)
\newcommand{\xcpy}{\ifasian{{\setmainfont{Lucida Bright}\copyright}}\else\copyright\fi}

\def\@translated{}
\def\atDatasheetHeadline{}

\ifdefined\atLiteratureNumber\def\atanyversionnumber{1}\fi
\ifx\theVersion\@empty\else\def\atanyversionnumber{1}\fi

\def\printversion{\ifdefined\atLiteratureNumber Document Number:\,\atLiteratureNumber\ifdefined\atLiteratureRevision\atLiteratureRevision\fi\else\ifx\theVersion\@empty\else Document Revision \theVersion\fi\fi}
\def\printversionnumber{\ifdefined\atLiteratureNumber\atLiteratureNumber\ifdefined\atLiteratureRevision\atLiteratureRevision\fi\else\ifx\theVersion\@empty\else\theVersion\fi\fi}

\newcommand{\titlefont}[1]{\huge\sffamily#1}
\newcommand{\Titlefont}[1]{\Huge\sffamily#1}
\newcommand{\Authorfont}[1]{\huge\sffamily#1}
\renewcommand{\maketitle}{ 
  \calccentering{\unitlength}
  \ifprintedbook
    \thispagestyle{empty}
    \begin{center}
    \noindent\\[4cm]{\Titlefont{\atTheTitle}}\\[1em]\rule{\linewidth}{1.0mm}\\[6em]
    \Authorfont{\@author}\\
    \vspace*{\fill}
    \includegraphics{xmoslogo18blk}
    \end{center}
    \cleardoublepage
	\makepubpage
  \else
    \ifonline\pdfMakeTitle\pdfMakeAuthor\makeDMSHook\fi
    \thispagestyle{footeronly}
    \parindent=0mm
    \parskip=3mm
	\begin{fullwidth}
	\noindent\\[4cm]{\ifmanual\Titlefont\else\titlefont\fi{\ifdatasheet\ifx\atDatasheetHeadline\@empty\atTheTitle\else\atDatasheetHeadline\fi\else\atTheTitle\fi}}\\\rule{\linewidth}{1.0mm}
    % Add headline if present
    \ifdatasheet\ifx\atDatasheetHeadline\@empty\else\vspace*{-20pt}\begin{flushright}\large\atTheTitle\end{flushright}\fi\fi
    % Add literature number of version number if present
    \ifdefined\atanyversionnumber\vspace*{-20pt}\begin{flushright}{\printversion}\end{flushright}\else\mbox{}\\[1em]\fi
    \begin{minipage}[t]{0.8\textwidth}
	\begin{flushleft}\noindent
  	% Add tools version if appropriate
	\ifdefined\atToolsVersionNumber\large{Tools Version: \textsf{\atToolsVersionNumber}}\\[0.5cm]\fi
	% Add authors
    \ifx\@author\@empty\else\large{Authored by: \textsf{\@author}}\\[0.5cm]\fi
    \ifx\atTheNotes\@empty\else\textsf{\atTheNotes}\\[0.5cm]\fi
    \ifx\@theBookInPrint\@empty\else\ifx\@translated\@empty\mbox{}\\[0.5cm]\else\vspace*{0.1cm}\fi \\\htmladdnormallink{Also available for purchase as a high quality printed book}{\@theBookInPrint}\fi
    \end{flushleft}
	\end{minipage}
    % Footer at bottom
	\vfill\noindent\\
    % Footer: Publication Date and Copyright Notice
	\ifnodms\textsf{Publication Date: \atTheDate}\\[0.1cm]\fi
    \end{fullwidth}
	\def\@notinpstool{}
	\newpage
  \fi
}

% Provide literature number to DSM; also provide location to stamp publication information
\ifarticle
\newcommand{\makeDMSHook}{\hypersetup{pdfkeywords={\ifdefined\atLiteratureNumber DOCNUM:\atLiteratureNumber\ifdefined\atLiteratureRevision\atLiteratureRevision\fi\fi,FOOTER:10,62,25;RELEASE:1,10,61,104,Publication Date: \$DATE;}}}
\else\ifmanual
\newcommand{\makeDMSHook}{\hypersetup{pdfkeywords={\ifdefined\atLiteratureNumber DOCNUM:\atLiteratureNumber\ifdefined\atLiteratureRevision\atLiteratureRevision\fi\fi,FOOTER:9,50,30;RELEASE:1,9,51,106,Publication Date: \$DATE;}}}
\fi\fi

% Publication details for printed books
\ifprintedbook
\newcommand{\publicationyears}[1]{\def\atThePublicationYears{#1}} \publicationyears{}
\newcommand{\impressions}[1]{\def\atTheImpressions{#1}} \impressions{}
\newcommand{\isbn}[1]{\def\atTheISBN{#1}} \isbn{}
\newcommand{\isbnpbk}[1]{\def\atTheISBNpbk{#1}} \isbnpbk{}
\newcommand{\isbnorg}[1]{\def\atTheOriginalISBN{#1}} \isbnorg{}
\fi

% Fonts and Paragraph
% See localiastion files for non-English font/paragraph settings
\ifonline\ifen\renewcommand*\familydefault{\sfdefault}\fi\fi
\def\Scriptsize{\fontsize{6pt}{6pt}\selectfont}
\def\Tiny{\fontsize{4pt}{4pt}\selectfont}
\def\TINY{\fontsize{3pt}{3.5pt}\selectfont}

\ifen
\RequirePackage[T1]{fontenc}
%\RequirePackage[altbullet]{lucidabr}
\renewcommand*\ttdefault{cmtt}
\newcommand{\CloverLeaf}{CL}
\ifonline
\nonzeroparskip
\parindent=0mm
\fi
\else
\RequirePackage{fontspec,xunicode,xltxtra}
\RequirePackage{xCJK}
%\RequirePackage{CJKpunct}
%\punctstyle{plain}
\XeTeXinputencoding "bytes"
\XeTeXdefaultencoding "bytes"
\fi
%\fi

% Must call package after setting fonts - changes single quotes 
% to straight line in verbatim/verb environments, as expected 
% for program listings
\RequirePackage{upquote}

% Chapter/section style
\ifarticle
\setsecheadstyle{\sffamily\LARGE\bfseries\raggedright}
\else\ifmanual
\setsecheadstyle{\sffamily\LARGE\bfseries\raggedright}
\setsubsecheadstyle{\sffamily\large\bfseries\raggedright}
\setsubsubsecheadstyle{\sffamily\bfseries\raggedright}
\else\ifbook
\setsecheadstyle{\sffamily\Large\bfseries\raggedright}
\setsubsecheadstyle{\sffamily\large\bfseries\raggedright}
\setsubsubsecheadstyle{\sffamily\bfseries\raggedright}
\fi\fi\fi

\ifdatasheet
% Make space between section title and first line of paragraph fixed (not rubber) 
% so that we can relocated text there for small headings
\newlength{\fixedsecskip}
\setlength{\fixedsecskip}{\onelineskip-0.7mm}
\setaftersecskip{\fixedsecskip}
\newcommand{\narrowsecname}{\vspace*{-8.7mm}}
\fi

% Header and Footer

\def\vhrulefill#1{\leavevmode\leaders\hrule\@height#1\hfill \kern\z@}

\newlength{\xmoslogolength}

\setlength{\headwidth}{\textwidth}
\ifprintedbook
\addtolength{\headwidth}{\marginparsep}
\addtolength{\headwidth}{\marginparwidth}
\else\ifmanual
\addtolength{\headwidth}{\marginparsep}
\addtolength{\headwidth}{\marginparwidth}
\fi\fi

\newlength{\footernologolength}
\newlength{\footerpartlinelength}
\setlength{\footernologolength}{\headwidth}
\setlength{\footerpartlinelength}{\footernologolength/2}

\makepagestyle{singlepage}
\makerunningwidth{singlepage}{\headwidth}
\makeheadrule{singlepage}{\headwidth}{1.2pt}
\makeheadposition{singlepage}{flushright}{flushright}{flushrught}{flushright}
\makepsmarks{singlepage}{%
 \nouppercaseheads
 \createmark{chapter}{both}{nonumber}{}{}
 \createmark{section}{right}{shownumber}{}{\quad}
 \createplainmark{toc}{both}{\contentsname}
 \createplainmark{lof}{both}{\listfigurename}
 \createplainmark{lot}{both}{\listtablename}
 \createplainmark{bib}{both}{\bibname}
 \createplainmark{index}{both}{\indexname}
 \createplainmark{glossary}{both}{\glossaryname}
} 
\newcommand{\headerfont}[1]{{\bfseries\sffamily#1}}
\newcommand{\footerfont}[1]{{\bfseries\sffamily#1}}
\ifdatasheet
\makeoddhead{singlepage}{\headerfont{\ifx\atTheTitle\@empty\else\atTheTitle\fi}}{}{\headerfont{\thepage}} 
\else
\makeoddhead{singlepage}{\headerfont{\ifx\atTheTitle\@empty\else\atTheTitle\fi \ifdefined\atToolsVersionNumber\ \emph{for tools version \atToolsVersionNumber}\fi}}{}{\headerfont{\thepage/\ifonline\hypersetup{linkcolor=black}\fi{\pageref{LastPage}}}} 
\fi
\makeoddfoot{singlepage}{}{\mbox{}\\[\onelineskip]\rule[2mm]{\footerpartlinelength}{1.2pt}\rule[2mm]{\footerpartlinelength}{1.2pt}\\\vspace*{-0.8em}\raggedleft\scriptsize\printversion}{}

% Double Page
\makepagestyle{doublepage}
\makerunningwidth{doublepage}{\headwidth}
\makeheadrule{doublepage}{\headwidth}{\normalrulethickness}
\ifmanual
% On double-page manual spreads, don't switch
\makeheadposition{doublepage}{flushright}{flushright}{}{}
\else
\makeheadposition{doublepage}{flushright}{flushleft}{}{}
\fi
\makepsmarks{doublepage}{%
\nouppercaseheads
 \createmark{chapter}{both}{nonumber}{}{}
 \createmark{section}{right}{shownumber}{}{\quad}
 \createplainmark{toc}{both}{\contentsname}
 \createplainmark{lof}{both}{\listfigurename}
 \createplainmark{lot}{both}{\listtablename}
 \createplainmark{bib}{both}{\bibname}
 \createplainmark{index}{both}{\indexname}
 \createplainmark{glossary}{both}{\glossaryname}
}
\ifmanual
\makeevenhead{doublepage}{\textsf{\bfseries\thepage\textsf\quad\bfseries\leftmark}}{}{}
\else
\makeevenhead{doublepage}{\textsf{\headerfont{\thepage}}}{}{\headerfont{\leftmark}}
\fi
\makeoddhead {doublepage}{\textsf{\headerfont{\rightmark}}}{}{\headerfont{\thepage}}

\makepagestyle{footeronly}
\makerunningwidth{footeronly}{\headwidth}
\makeheadposition{footeronly}{flushright}{flushright}{flushrught}{flushright}
\makeoddfoot{footeronly}{}{\mbox{}\\[\onelineskip]\rule[2mm]{\footerpartlinelength}{1.2pt}\rule[2mm]{\footerpartlinelength}{1.2pt}}{}
% fix rename to firstpagefooter

\makepagestyle{footerline}
\copypagestyle{footerline}{singlepage}
\ifmanual
\makeoddfoot{footerline}{}{\mbox{}\\[\onelineskip]\rule[-0.6pt]{\headwidth}{1.2pt}}{}
\else
\makeoddfoot{footerline}{}{\mbox{}\\[\onelineskip]\rule[1.2pt]{\headwidth}{1.2pt}}{}
\fi

\copypagestyle{nofoot}{singlepage}
\makeoddfoot{nofoot}{}{}{}

\ifonline
% fix: why isn't empty cutting it here?
\copypagestyle{plain}{singlepage}
\makeheadrule{plain}{\headwidth}{0pt}
\makeoddhead{plain}{}{}{}
\else
\makeevenfoot{plain}{}{}{}
\makeoddfoot{plain}{}{}{}
\fi

\ifprintedbook
\pagestyle{doublepage}
\else
\pagestyle{singlepage}
\fi

% Double Page Clear
\newcommand{\clearemptydoublepage}{\newpage{\thispagestyle{plain}\cleardoublepage}}
%\let\origdoublepage\cleardoublepage
%\newcommand{\clearemptydoublepage}{%
%\clearpage%
%\ifonline\else{\pagestyle{empty}\origdoublepage}\fi%
%}

% Table of Contents Settings
\newcommand{\toc}{{\parskip=0mm\begin{fullwidth}\tableofcontents*\end{fullwidth}}\ifbook\clearemptydoublepage\fi}
\newcommand{\tocValued}{\toc\vspace\fill\AddedMyOwnDisclaimer\valuedcustomer\newpage}
\ifbook
% Extend Page Window on Table of Contents
% to support books with over 100 pages.
\makeatletter
\renewcommand{\@pnumwidth}{1.9em}
\makeatother
\maxtocdepth{subsection}
\fi
\ifmanual
\renewcommand{\tocheadstart}{}
\renewcommand{\contentsname}{Table of Contents}
\renewcommand{\printtoctitle}[1]{\LARGE\bfseries #1}
\renewcommand{\afterchaptertitle}{\vskip\onelineskip}
\renewcommand{\aftertoctitle}{\thispagestyle{singlepage}\afterchaptertitle}
\fi

% Forced Indentation
\newlength\forceindentlen
\setlength\forceindentlen{18pt}
\ifonline
\newcommand{\forceindent}{\hspace*{\forceindentlen}}
\else
\newcommand{\forceindent}{\indent}
\fi
\newcommand{\forcelargeindent}{\forceindent\forceindent\forceindent}

% Program Environment
\floatstyle{ruled}
\newfloat{program}{thp}{lop}
\floatname{program}{Program}

% Named lists
\newenvironment{Ventry}[1]%
{\begin{list}{}{\renewcommand{\makelabel}[1]{\textbf{##1}\hfil}%
\settowidth{\labelwidth}{\textbf{#1}}%
\setlength{\leftmargin}{\labelwidth + \labelsep}}}%
{\end{list}}

% Hline
\newlength\savedwidth
\newcommand\Hline{\noalign{\global\savedwidth\arrayrulewidth\global\arrayrulewidth 1.8pt}\hline\noalign{\global\arrayrulewidth\savedwidth}}

\definecolor{arrowcolor}{gray}{0.6}

% Enumerations with first indent flush to left margin
\newlist{steps}{enumerate}{1}
\setlist[steps]{leftmargin=*, labelindent=\parindent, topsep=0pt, partopsep=0pt, label=\arabic*.}

% FIXED: used to be \textbullet
\newlist{points}{itemize}{1}
\setlist[points]{leftmargin=*, labelindent=\parindent, topsep=0pt, partopsep=0pt, label=\color{arrowcolor}{\Forward}}

\newlist{actions}{itemize}{1}
\setlist[actions]{leftmargin=*, labelindent=\parindent, topsep=0pt, partopsep=0pt, label=\Forward}

\newlist{functions}{itemize}{1}
\setlist[functions]{leftmargin=*, labelindent=\parindent, topsep=0pt, itemsep=1em, label=\Forward}
\newcommand{\itemfunc}[1]{\item \texttt{#1}}
\newcommand{\func}[1]{\begin{sloppypar}\texttt{\textbf{#1}}\end{sloppypar}}

% FIX: deleted
%\newlist{nopoints}{itemize}{1}
%\setlist[nopoints]{leftmargin=0pt, labelindent=0pt, label=}

% FIX: deleted
%\RequirePackage{rotating}
%\newlist{ticks}{itemize}{1}
%\setlist[ticks]{leftmargin=*, labelindent=\parindent, label=\begin{turn}{-15}\CheckmarkBold\end{turn}}
%\newenvironment{checklist}{%
%\renewcommand{\tabcolsep}{0pt}
%\setlength{\LTpre}{0em}
%\setlength{\LTpost}{0em}
%\noindent\begin{longtable}{lp{\textwidth-0.7cm}}
%}
%{\end{longtable}}
%\definecolor{greybar}{gray}{0.8} % fix: changed ok now
%\newcommand{\checkarrow}{{\color{arrowcolor}{\vline\vline\vline\vline\vline\vline\vline\vline}} \color{arrowcolor}{\Forward}\ & }
%newcommand{\checknl}{\\[\onelineskip]}

\newlist{arrow}{itemize}{1}
\setlist[arrow]{leftmargin=*, label=\color{arrowcolor}{\Forward}, topsep=0pt, itemsep=0.4em, partopsep=0pt}

\newlist{features}{itemize}{3}
\setlist[features]{leftmargin=*, label=\Forward, topsep=0pt, itemsep=0.2em, partopsep=0pt}
\setlist[features,1]{font=\bfseries}
\setlist[features,2]{label=\color{arrowcolor}{\textbullet}, itemsep=0em, topsep=-0.15em, beginpenalty=1000, midpenalty=1000}
\setlist[features,3]{label={---}, itemsep=0em, beginpenalty=10000, midpenalty=10000}

\newlist{revisions}{enumerate}{2}
\setlist[revisions,1]{leftmargin=*, labelindent=0mm, itemsep=2em, font=\bfseries, label=Rev.}
\setlist[revisions,2]{leftmargin=3mm, labelindent=\parindent, label=\arabic*., beginpenalty=1000, midpenalty=1000}

\newlist{Lentry}{description}{1}
\setlist[Lentry]{font=\normalfont, style=nextline, leftmargin=50pt, noitemsep}
\newenvironment{itempars}{\parskip=\itemxskip}{}

\newenvironment{block-itemize}{%
  \itemize
  \let\my@olditem\item
  \let\my@closepage\relax  
  \def\item{%
    \my@closepage\my@olditem\minipage[t]{\textwidth}%
    \let\my@closepage\endminipage
  }%
}{\my@closepage\enditemize}


% Unix-style Options
\newlist{option}{description}{1}
\setlist[option]{font=\ttfamily, style=nextline, leftmargin=50pt, noitemsep}
\newcommand{\optemph}[1]{\textsf{\textit{#1}}}
\newcommand{\itemx}[1]{%
  \setlength{\itemsep}{10pt}
  \item[#1]
  \setlength{\itemsep}{0pt}
}
\newcommand{\itemy}[1]{\item[#1]}
\newlength{\itemxskip}
\setlength{\itemxskip}{\onelineskip/2}
\newcommand{\itemnl}{\mbox{}\\[\itemxskip]}
\newcommand{\optind}{\hspace{35pt}}

% Fancy layout for 'In this chapter'
\newlength{\inthischapterbot}
\setlength{\inthischapterbot}{-\onelineskip+0.4em}
\newlength{\inthischapterskip}
\setlength{\inthischapterskip}{\onelineskip}
\newenvironment{inthischapter}%
  {\begin{fullwidth}
  {\noindent\color{arrowcolor}{\rule{\linewidth}{0.06cm}}}\\[0.4em]
  \noindent\textsf{\textbf{In This Chapter}}
  \begin{arrow}}%
  {\end{arrow}\vspace*{\inthischapterbot}
  {\color{arrowcolor}{\rule{\linewidth}{0.06cm}}}\\[\inthischapterskip]
  \end{fullwidth}
  \par}

% XC Syntax
\newlength{\codeindent}
\setlength{\codeindent}{30pt}
\lstdefinelanguage{XC} {sensitive=true, morestring=[b]",}
\lstset{frame=leftline,framerule=0pt,showspaces=false,showstringspaces=false,
   showtabs=false,keywordstyle=\bfseries,%
   %escapechar=\%,
   literate={@}{{\tiny{\MVAt}}}1,
   xleftmargin=\codeindent,xrightmargin=0pt,language=XC,basicstyle=\ttfamily\small}

\newcommand{\command}[1]{\begin{features}\item \texttt{#1}\end{features}}
%\newcommand{\command}[1]{\par\hspace*{\codeindent}\texttt{#1}\par}
\newlength{\gdbpwidth}
\settowidth{\gdbpwidth}{(gdb) }
\newlength{\gdbpwidthb}
\setlength{\gdbpwidthb}{\codeindent-\gdbpwidth}
\newcommand{\gdbcommand}[1]{(gdb) \hspace*{\gdbpwidthb}\texttt{#1}}
\newcommand{\xtacommand}[1]{> \hspace*{\gdbpwidthb}\texttt{#1}}

% Colors
\definecolor{black}{rgb}{0,0,0}
\definecolor{white}{rgb}{1,1,1}
\definecolor{yell}{rgb}{1,0.847,0.118}
\definecolor{darkgreen}{rgb}{0,0.7,0}
\definecolor{darkblue}{rgb}{0,0,0.6}

\definecolor{brightred}{rgb}{1.00, 0.12, 0.00}
\definecolor{brightgreen}{rgb}{0.02, 0.98, 0.00}
\definecolor{brightblue}{rgb}{0.20, 0.41, 1.00}

\definecolor{pastelyell}{rgb}{1.00, 1.00, 0.60}
\definecolor{pastelpink}{rgb}{0.80, 0.62, 1.00}
\definecolor{pastelgreen}{rgb}{0.79, 0.99, 0.80}
\definecolor{pastelorange}{rgb}{1.00, 0.80, 0.60}
\definecolor{pastelblue}{rgb}{0.59, 0.80, 1.00}

\definecolor{paleblue}{rgb}{0.80, 1.00, 1.00}
\definecolor{babyblue}{rgb}{0.79, 1.00, 1.00}

\definecolor{lightgrey}{gray}{0.93}
\definecolor{darkgrey}{gray}{0.3}

% Symbols

% New define for tt for internationalisation of tt fonts
\newcommand{\Texttt}[1]{\texttt{#1}}

%\newcommand{\ttsquote}{\verb+'+ } % requires upquote (see below) 
\newcommand{\seesec}[1]{\emph{see} \Sec~\ref{#1}}
\newcommand{\seesecnum}[1]{\emph{see} \Sec~#1}
\newcommand{\seefig}[1]{\emph{see} \figurename~\ref{#1}}
\newcommand{\Sec}{\S$\!\!$}
\newcommand{\Y}{\ding{51}} % requires pifont, fix move to here
\newcommand{\N}{\ding{55}} % requires pifont, fix move to here
\newcommand{\ttbslash}{\texttt{\char`\\}}
\newcommand{\ttlbrace}{\texttt{\char`\{}}
\newcommand{\ttrbrace}{\texttt{\char`\}}}
\newcommand{\ttcaret}{\textasciicircum}
\newcommand{\tildesym}{\textasciitilde}
\newcommand{\lebnf}{$\langle$}
\newcommand{\rebnf}{$\rangle$}
\newcommand{\escape}[1]{\Texttt{\ttbslash #1}}
\newcommand{\token}[1]{\textnormal{\texttt{#1}}}
\newcommand{\newinxc}{${\textrm{\small{\textsf{NEW}}}\atop{\textrm{\colorbox{black}{\color{white}\small{\textsf{XC}}}}}}$}
\newcommand{\optionalS}[1]{\ifthenelse{#1 > 1}{s}{}}

% Make sure memoir side captions don't break articles/books
\ifmanual\else
\makeatletter
\def\@@sidecaption#1#2[#3]{\caption{#2}{\label{#3}}}
\def\endsidecaption{}
\makeatother
\fi

% Margin Symbols (fix this is not online/offline issue)
\ifonline
\newcommand{\cautionmargin}{\reversemarginpar\marginpar{\flushright{\lhdbend}}\ifen\ \fi}
\newcommand{\pencilmargin}{\reversemarginpar\marginpar{\flushright{\huge{\ding{46}}}}\ifen\ \fi}
\newcommand{\newinxcmargin}{\reversemarginpar\marginpar{\flushright{\huge{\newinxc}}}\ifen\ \fi}
\newcommand{\icomargin}[1]{\reversemarginpar\marginpar{\flushright{\marginnote{\includegraphics{#1}}}}}
\else
\strictpagechecktrue
\newcommand{\xisodd}[2]{\strictpagechecktrue\checkoddpage\ifoddpage \textbf{#1} \else \textbf{#2} \fi}
\newcommand{\cautionmargin}{\xisodd{\marginpar{\hfill\lhdbend}\ifasian\!\fi}{\marginpar{\lhdbend}}\ifasian\!\fi}
\newcommand{\pencilmargin}{\xisodd{\marginpar{{\raisebox{-4mm}{\huge{\ding{46}}}}}}{\marginpar{\raggedleft{\raisebox{-4mm}{\huge{\ding{46}}}}}}}
\newcommand{\newinxcmargin}{\xisodd{\marginpar{\hfill\newinxc}\ifasian\!\fi}{\marginpar{\newinxc}\ifasian\!\fi}}
\newcommand{\icomargin}[1]{\xisodd{\reversemarginpar{\marginnote{\includegraphics{#1}}}}{\marginnote{\includegraphics{#1}}}}
\fi

% Table tightness, default to usual values
\newcommand{\loosertables}{\renewcommand{\arraystretch}{1.40}}
\newcommand{\loosetables}{\renewcommand{\arraystretch}{1.25}}
\newcommand{\tighttables}{\renewcommand{\arraystretch}{1.00}} %default
\ifarticle
\loosetables
\else\ifmanual
\loosetables
\fi
\fi

% Captions
\ifmanual
\precaption{\ifthenelse{\@infullwidth=0}{\rule{\linewidth}{0.06cm}\\[0.3em]\raggedleft}{}}
\postcaption{\vspace{-0.2em}\ifthenelse{\@infullwidth=0}{\rule{\linewidth}{0.06cm}}{}}
\captionwidth{\marginparwidth}
\captiondelim{:\ifthenelse{\@infullwidth=0}{\\[-\onelineskip]}{\ }}
\captionstyle{\ifthenelse{\@infullwidth=0}{\raggedleft}{\raggedright}}
\captionnamefont{\bfseries\sffamily\small}
\captiontitlefont{\sffamily\small}
\setsidecaps{\marginparsep}{\marginparwidth}
\sidecapmargin{left}
\setsidecappos{b}
\renewcommand*{\sidecapstyle}{\captionstyle{\raggedleft\small}}
\fi

\newcommand{\tablecaption}[2][\@empty]{
\captionnamefont{\ifen\scshape\fi\hfill}
\captiondelim{\hfill}
\captionstyle{\centerlastline\\}
\ifen\captiontitlefont{\scshape}\fi
\setlength{\belowcaptionskip}{10pt}
\ifx #1\@empty \caption{#2}\else \caption[#1]{#2}\fi}

\newcommand{\fullwidthcaption}[2][\@empty]{
\captionnamefont{\ifen\scshape\fi\hfill}
\captiondelim{\hfill}
\captionstyle{\centerlastline\\}
\ifen\captiontitlefont{\scshape}\fi
\setlength{\belowcaptionskip}{10pt}
\ifx #1\@empty \caption{#2}\else \caption[#1]{#2}\fi}

\newlength{\widelength}
\setlength{\widelength}{0.7in}

% Fix: remove xcsyntax environment once updated in rst generator
\newlength{\syntaxlen}
\newenvironment{grammar}[1]{\settowidth{\syntaxlen}{#1\ }\begin{em}\hspace*{\blockindentlen}\small\begin{tabular}{@{}p{\syntaxlen}@{~}c@{~~}l}}{\end{tabular}\end{em}}%
\newenvironment{xcsyntax}[1]{\settowidth{\syntaxlen}{#1\ }\begin{em}\hspace*{\blockindentlen}\small\begin{tabular}{@{}p{\syntaxlen}@{~}c@{~~}l}}{\end{tabular}\end{em}}%
\newcommand{\ebnf}[2]{\ifthenelse{\equal{#1}{opt}}{#2$_{\mathrm{\emph{opt}}}$}{\ifthenelse{\equal{#1}{0}}%
   {\lebnf#2\rebnf$^*$}{\ifthenelse{\equal{#1}{1}}{\lebnf#2\rebnf$^\textrm{\tiny{+}}$}{ERROR}}}}
\newcommand{\is}{\texttt{\em:\hspace*{-2pt}:\hspace*{-1pt}=}}
\newcommand{\choice}{\texttt{\em |}}
\newcommand{\oneof}{\textit{one of}}
\newcommand{\opsep}{~~~}
\newcommand{\xclang}[1]{\textit{#1}}

\newcommand{\linkdesc}[2]{\ifonline\htmladdnormallink{#2}{#1}\else#1\fi}
\newcommand{\xurldesc}[2]{\ifonline\htmladdnormallink{\textbf{#2}}{#1}\else\textbf{#1}\fi}
\newcommand{\xurl}[1]{\xurldesc{#1}{\texttt{#1}}}
\newcommand{\shortcut}[1]{\emph{#1}}
\newcommand{\linkdocnum}[1]{\linkdesc{http://www.xmos.com/docnum/#1}{#1}}
\newcommand{\documentnumber}[1]{document number \linkdocnum{#1}}
\newcommand{\trianglenote}[1]{\begin{features}\item #1\end{features}}
\newcommand{\triangleurl}[1]{\trianglenote{\xurl{#1}}}

% Specifications (fix - move to xcuser guide as this is only place used)
\newenvironment{spec}{\small\lstset{basicstyle=\ttfamily\footnotesize,xleftmargin=10pt}}{\normalsize\lstset{basicstyle=\ttfamily\small,xleftmargin=\codeindent}}

% Terms
\input{terminology}

% Welcome (fix - move to xcuser guide as this is only place used)
\newcommand{\welcome}[1]{\ifonline\else%
\chapter*{#1}%
\markboth{#1}{#1}%
\input{welcome}%
\clearemptydoublepage%
\fi}

% Bibliography
\input{bib}
\bibliographystyle{unsrt}
\newcommand{\xmosbib}{\bibliography{xmos}}

\ifbook\else\renewcommand*{\bibname}{Related Documents}\fi
\ifnochapters
% Ensure bibliography is a standard numbered section
\renewcommand{\bibsection}{\section{\bibname}}
\else
\renewcommand{\bibsection}{%
\chapter{\bibname}
\bibmark
%\ifnobibintoc\else
%\phantomsection
%\addcontentsline{toc}{chapter}{\bibname}
%\fi
\prebibhook
}
\fi

\renewenvironment{thebibliography}[1]{%
\bibsection
\ifmanual\begin{fullwidth}\fi
\begin{bibitemlist}{#1}}%
{\end{bibitemlist}\ifmanual\end{fullwidth}\fi\postbibhook}

% Index
\newcommand{\xmosindex}{\begin{footnotesize}\printindex\newpage\end{footnotesize}}
\newcommand{\indexheadchar}[1]{\ifthenelse{\equal{#1}{Symbols}}{}{%
                               \ifthenelse{\equal{#1}{Default}}{}{%
                               {\bfseries\large\sffamily\quad\quad #1}}}}

% Literature Numbers
\newcommand{\docnum}[2]{\def\atLiteratureNumber{#1}\setcounter{revcounter}{#2}\def\atLiteratureRevision{\Alph{revcounter}}}

% Tools Version
\newcommand{\toolsversion}[1]{\def\atToolsVersionNumber{#1}}

% Revisions
\newtoks{\revisiontoks}  
\revisiontoks={}
\def\revisionflag{0}
\def\activeflag{1}
\newcounter{revcounter}
\setcounter{revcounter}{0}
% FIX depricate
\newcommand{\setLatestRevision}[1]{\setcounter{revcounter}{#1}\def\atLiteratureRevision{\Alph{revcounter}}}
\newcommand{\pushRevision}[1]{\revisiontoks=\expandafter{\the\revisiontoks\item #1}\def\revisionflag{1}}
\newcommand{\popRevisions}[1]{\ifthenelse{\equal{\activeflag}{1}}{\ifthenelse{\equal{\revisionflag}{1}}{\ifthenelse{\value{revcounter}>0}{\item\textbf{\atLiteratureNumber\Alph{revcounter}--#1}\addtocounter{revcounter}{-1}\begin{revisions}\the\revisiontoks\end{revisions}\revisiontoks={}\def\revisionflag{0}}{\item ERROR: Not enough revision numbers\def\revisionerror{1}}}{}}{}}

% Final Typesetting
% changes to page length
\newcommand{\pfinallongpage}{\ifonline\else\enlargethispage{\baselineskip}\fi}
\newcommand{\pfinalshortpage}{\ifonline\else\enlargethispage{-\baselineskip}\fi}
\newcommand{\pfinalforcedpage}{\ifonline\else\enlargethispage*{\baselineskip}\fi}
% correct latex's decision about when to start a new page
\newcommand{\pfinalpagebreak}{\ifonline\else\pagebreak\fi}
\newcommand{\pfinalnewpage}{\ifonline\else\newpage\fi}
% add or subtract tiny bits of vertical space to improve visual appearance
\newcommand{\pfinalfixedskip}[1]{\ifonline\else\vspace*{#1}\fi}
\newcommand{\pfinalfill}{\ifonline\else\vspace*{\fill}\fi}
\newcommand{\pfinalnewline}{\ifonline\else\newline\fi}
\newcommand{\pfinalspace}{\ifonline\else\ \fi}

\newcommand{\wfinallongpage}{\ifonline\enlargethispage{\baselineskip}\fi}
\newcommand{\wfinalshortpage}{\ifonline\enlargethispage{-\baselineskip}\fi}
\newcommand{\wfinalforcedpage}{\ifonline\enlargethispage*{\baselineskip}\fi}
% correct latex's decision about when to start a new page
\newcommand{\wfinalpagebreak}{\ifonline\pagebreak\fi}
\newcommand{\wfinalnewpage}{\ifonline\newpage\fi}
% add or subtract tiny bits of vertical space to improve visual appearance
\newcommand{\wfinalfixedskip}[1]{\ifonline\vspace*{#1}\fi}
\newcommand{\wfinalfill}{\ifonline\vspace*{\fill}\fi}
\newcommand{\wfinalkillfooter}{\ifonline\thispagestyle{nofoot}\fi}

\newcommand{\finalchapter}[2]{\ifonline\setlength{\afterchapskip}{#2\baselineskip}\fi\chapter{#1}\ifonline\setlength{\afterchapskip}{5\baselineskip}\fi}

\newcommand{\finalmbox}[1]{\mbox{#1}}
\newcommand{\finallineadj}[1]{\mbox{#1}}

%\printinunitsof{mm}
%\stockvalues
