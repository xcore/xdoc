% XCore xdoc LaTeX class file

\NeedsTeXFormat{LaTeX2e}[1995/12/01]
\ProvidesClass{xcore}
              [2011/11/24 v1.0b Initial Release]
              
\DeclareOption*{\ClassError{xcore}{The `\CurrentOption' option is not supported}}

\newif\ifdocument\documenttrue
\newif\ifcollection\collectionfalse
\DeclareOption{document}{\documenttrue}
\DeclareOption{collection}{\documenttrue\collectiontrue}
\ProcessOptions

\LoadClass[oneside,onecolumn,article,10pt]{memoir}

% Set conservative values to prevent the need
% for too much manual typesetting
\widowpenalty=10000
\clubpenalty=10000
\renewcommand{\textfraction}{0.01}
\renewcommand{\topfraction}{0.99}

% PDF Properties
\RequirePackage{ifpdf}
\ifpdf
\pdfminorversion=5
\pdfobjcompresslevel=3
\pdfcompresslevel=9
\fi

% Needed for internal calculations
\RequirePackage{calc}

% Set the paper stock size
\setstocksize{235mm}{178mm}

% Set the trimmed size
\settrimmedsize{235mm}{178mm}{*}
\setlength{\trimtop}{0pt}
\setlength{\trimedge}{\stockwidth}
\addtolength{\trimedge}{-\paperwidth}

% Title width
\newlength{\titlewidth}
\setlength{\titlewidth}{135mm}

% Set the type block size
\newlength{\typeblockwidth}
\setlength{\typeblockwidth}{135mm}
\settypeblocksize{47\onelineskip}{\typeblockwidth}{*}

% Set the margins
\setlrmargins{*}{*}{1.0}

% Set the block indentation level
\newlength{\blockindentlen}
\setlength{\blockindentlen}{5mm}

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

% Part Styles
\renewcommand*{\thepart}{\Alph{part}}

% Chapter Styles
\RequirePackage[final]{graphicx}

\makechapterstyle{collection}{%
\setlength{\afterchapskip}{0pt}
\setlength{\beforechapskip}{8mm}
\setlength{\midchapskip}{\textwidth}
\addtolength{\midchapskip}{-\beforechapskip}
\renewcommand*{\chapterheadstart}{}
\renewcommand*{\chaptitlefont}{\huge\bfseries}
\renewcommand*{\chapnumfont}{\chaptitlefont}
\renewcommand*{\printchaptername}{}
\renewcommand*{\chapternamenum}{}
\renewcommand*{\afterchapternum}{}
\renewcommand*{\printchapternum}{}
\renewcommand*{\printchaptertitle}[1]{\thispagestyle{noheader}%
\begin{minipage}[t]{\beforechapskip}{\chapnumfont\thechapter}\end{minipage}%
\hfill\begin{minipage}[t]{\midchapskip}{\chaptitlefont ##1\par}\end{minipage}%
\\[3mm]}}
\renewcommand*{\afterchaptertitle}{}
\chapterstyle{collection}

% Only collections have chapters
\ifcollection\else\renewcommand*\thesection{\arabic{section}}\fi

% Number section depth up to X.Y.Z
\maxsecnumdepth{subsubsection}

% Footnote styles
\newfootnoteseries{P}
\renewcommand*{\@makefnmarkP}[1]{\slashfracstyle{(X #1)}}
\footmarkstyleP{#1--}

\setlength{\footmarkwidth}{1.8em}
\setlength{\footmarksep}{0em}
\footmarkstyleP{\MakeUppercase{#1}.\hfill}

\RequirePackage{amsmath}
\ifpdf
\RequirePackage[activate={true,nocompatibility},final]{microtype}
\DisableLigatures{encoding = T1, family = tt*} % Prevent \texttt{--} from becoming em-dash
\fi
\RequirePackage{stmaryrd}
\RequirePackage{alltt}
\RequirePackage{amsfonts}
\RequirePackage{tabularx}
\RequirePackage{ifthen}
\RequirePackage{longtable} 
\newcolumntype{Y}{>{\raggedright\arraybackslash}X}
\newcolumntype{y}{>{\small\raggedright\arraybackslash}X}
\RequirePackage{textcomp}
\RequirePackage{url}
\RequirePackage{listings}
\RequirePackage{gensymb} % provides generic symbol macros such as \micro
\RequirePackage{xspace}
\RequirePackage{multirow}
\RequirePackage{fixltx2e} % various fixes to latex2e
\RequirePackage{booktabs}
\RequirePackage{enumitem}
\RequirePackage{placeins} % defines \FloatBarrier command
\RequirePackage{flafter} % floats come after reference
\RequirePackage{marginnote} % works properly with \reversemarginpar to always use left margins 
\RequirePackage{marvosym} % provides \MVAt @ symbol and \forward
\RequirePackage{color}

% PDF Settings (must load after other packages)
\RequirePackage[hyperindex=true,hyperfootnotes=false]{hyperref}
\hypersetup{%
  pdfcreator         = {\LaTeX},
  pdfpagemode        = UseOutlines,
  pdfdisplaydoctitle = true,
  pdfstartview       = Fit,
  pdfpagelayout      = standardpage,
  breaklinks
}
\RequirePackage{memhfixc}
\hypersetup{colorlinks = true, linkcolor = blue, citecolor = blue, urlcolor = blue }

% Title Page
\renewcommand{\title}[1]{\def\atTheTitle{#1}\def\@pdfTitle{#1}} \title{}
\renewcommand{\maketitle}{ 
  \thispagestyle{noheader}
  \noindent\\[\ifcollection 4cm\else -1cm \fi]{\bfseries\ifcollection\Huge\else\huge\fi\atTheTitle}\\
  \ifcollection\newpage\else\vskip 2.5mm\fi
}

\newcommand{\version}[1]{\def\theVersion{#1}} \version{}
\newcommand{\yearmonthday}[3]{\def\atTheYear{#1}\def\atTheDate{#1/#2/#3}} \yearmonthday{\number\year}{\number\month}{\number\day}

% Document Boundaries
\newcommand{\start}{\begin{document}}
\newcommand{\finish}{\PrintDisclaimer\end{document}}

% Get the last page number
\RequirePackage{lastpage}

% Disclaimer
\newcommand{\PrintDisclaimer}{
  % Use trick to get to bottom of current or next page (if \needspace creates a short page it makes it flushbottom)
  \FloatBarrier % ensure all figures printed by this time
  \Needspace{3.3cm}
  \vspace*{\fill}
  \rule[1mm]{\linewidth}{1pt}
  \small
  The document is provided to you ``AS IS'' with no warranty of any
  kind, express or implied and shall have no liability in relation to
  its use. The author makes no representation that the information, or
  any particular implementation thereof, is or will be free from any
  claims of infringement and again, shall have no liability in
  relation to any such claims.
}

% Fonts and Paragraph
\RequirePackage[T1]{fontenc}
\renewcommand*\familydefault{\sfdefault}
\nonzeroparskip
\parindent=0mm
\def\Small{\fontsize{8pt}{9pt}\selectfont}
\def\Scriptsize{\fontsize{6pt}{6pt}\selectfont}

% Must call package after setting fonts - changes single quotes 
% to straight line in verbatim/verb environments, as expected 
% for program listings
\RequirePackage{upquote}

% Header and Footer
\makepagestyle{standardpage}
\makerunningwidth{standardpage}{\textwidth}
\makeheadrule{standardpage}{\textwidth}{1pt}
\makeheadposition{standardpage}{flushright}{flushright}{flushrught}{flushright}
\makepsmarks{standardpage}{%
 \nouppercaseheads
 \createmark{chapter}{both}{nonumber}{}{}
 \createmark{section}{right}{shownumber}{}{\quad}
} 
\makeoddhead{standardpage}{\textbf{\atTheTitle}}{}{\textbf{\thepage/\hypersetup{linkcolor=black}{\pageref{LastPage}}}}
\pagestyle{standardpage}

\makepagestyle{noheader}
\makerunningwidth{noheader}{\textwidth}
\makeheadposition{noheader}{flushright}{flushright}{flushrught}{flushright}

% Table of Contents Settings
\newcommand{\toc}{\tableofcontents*}

% Indentation
\newlength\forceindentlen
\setlength\forceindentlen{18pt}
\newcommand{\forceindent}{\forceindentlen}
\newcommand{\forcelargeindent}{\forceindent\forceindent\forceindent}
\newlength{\savedcodeindent}
\newenvironment{indentation*}[2]%
{\begin{indentation}{#1}{#2}
 \setlength{\savedcodeindent}{\codeindent}
 \addtolength{\codeindent}{#1}
}
{\setlength{\codeindent}{\savedcodeindent}
 \end{indentation}
}

% Commentary Environment
\newenvironment{commentary}{\begin{adjustwidth}{11mm}{}\begin{small}}{\end{small}\end{adjustwidth}}

% Lists

\newlist{steps}{enumerate}{1}
\setlist[steps]{label=(\arabic*)}

\newlist{compactsteps}{enumerate}{1}
\setlist[compactsteps]{label=(\arabic*), itemsep=0pt}

\newlist{points}{itemize}{1}
\setlist[points]{label=\textbullet}

\newlist{compactpoints}{itemize}{1}
\setlist[compactpoints]{label=\textbullet, itemsep=0pt}

\newlist{nopoints}{itemize}{1}
\setlist[nopoints]{leftmargin=0pt, labelindent=0pt, label=}

\newlist{compactnopoints}{itemize}{1}
\setlist[compactnopoints]{leftmargin=0pt, labelindent=0pt, itemsep=0pt, label=}

\newlist{actions}{itemize}{1}
\setlist[actions]{leftmargin=*, labelindent=\parindent, label=\textbullet}

\newlist{option}{description}{1}
\setlist[option]{font=\ttfamily, leftmargin=22mm, itemsep=0.5\baselineskip, parsep=0.5\baselineskip, style=nextline}
\newcommand{\duplicateoption}{\vspace*{-\baselineskip}} % fix, may not be robust between page breaks
\newcommand{\optemph}[1]{\textmd{\sffamily\textit{#1}}}

% Program Code
\newlength{\codeindent}
\setlength{\codeindent}{3pt}
\definecolor{framegray}{gray}{0.75}
\lstset{backgroundcolor=\color{lightgrey},aboveskip=\baselineskip,belowskip=3pt}
\lstset{%
   frame=single,framerule=0.4pt,rulecolor=\color{framegray}, rulesepcolor=\color{framegray},
   showspaces=false,showstringspaces=false,showtabs=false,
   keywordstyle=\bfseries,%
   %escapechar=\%,
   literate={@}{{\tiny{\MVAt}}}1,
   xleftmargin=\codeindent,xrightmargin=0pt,basicstyle=\ttfamily\small}
% \lstset{prebreak=\raisebox{-0.5ex}[0ex][0ex]
%   {{\normalsize \ensuremath{\hookleftarrow}}}}
 \lstset{postbreak=\raisebox{0ex}[0ex][0ex]
   {{\normalsize \ensuremath{\hookrightarrow\space}}}}
 \lstset{breaklines=true, breakindent=10pt}



% Command
\newcommand{\command}[1]{\par\texttt{#1}\par}

% Colors
\definecolor{black}{rgb}{0,0,0}
\definecolor{white}{rgb}{1,1,1}
\definecolor{brightred}{rgb}{1.00, 0.12, 0.00}
\definecolor{lightgrey}{gray}{0.935}

% Symbols
\newcommand{\Sec}{\S$\!\!$}
\newcommand{\newinxc}{${\textrm{\small{\textsf{NEW}}}\atop{\textrm{\colorbox{black}{\color{white}\small{\textsf{XC}}}}}}$}
\newlength{\cloverleafheight}\newcommand{\CloverLeaf}{\settoheight\cloverleafheight{\textsf{]}}\includegraphics[height=\cloverleafheight]{cloverleaf.pdf}\xspace}

% Margin Symbols

% The ideal height of an icon on a single line is one baselineskip
% The ideal height of an icon on n lines is (n-1)baselineskip + height of ]
\newlength{\iconht}
\newcommand{\calciconspace}[1]{\ifthenelse{\equal{#1}{1}}{\setlength\iconht{\baselineskip}}{%
\settoheight\iconht{\textsf{]}}\addtolength\iconht{#1\baselineskip}\addtolength\iconht{-\baselineskip}}}
\newlength{\iconadj}
\newlength{\iconadjraise}
\newlength{\icongap}
\newlength{\iconcenter}
% Adjust for icons to align with top of text on first line
% Sometimes want to vertically center on a single line too
\newcommand{\calciconadj}{\settoheight\iconadj{\textsf{]}}\setlength\iconadj{-\iconadj}%
\setlength{\icongap}{\iconht+\iconadj}%
\setlength{\iconcenter}{\icongap/2}%
\setlength\iconadjraise{\iconadj-\iconcenter}}

\newcommand{\newinxcmargin}{\reversemarginpar\marginpar{\flushright{\huge{\vspace*{-0.21cm}\newinxc}}}\ }
\newcommand{\newinxcmarginraise}{\newinxcmargin}

\newcommand{\iconmargin}[2]{%
\calciconspace{#1}\calciconadj%
\reversemarginpar\marginpar{\hfill\vtop{\vskip\iconadj%
\hbox{\includegraphics[height=\iconht]{#2}}}}\xspace}

\newcommand{\iconmarginraise}[2]{%
\calciconspace{#1}\calciconadj%
\reversemarginpar\marginpar{\hfill\vtop{\vskip\iconadjraise%
\hbox{\includegraphics[height=\iconht]{#2}}}}\xspace}

\newcommand{\doubleiconmargin}[3]{%
\calciconspace{#1}\calciconadj%
\reversemarginpar\marginpar{\hfill\vtop{\vskip\iconadj%
\hbox{\includegraphics[height=\iconht]{#2} \includegraphics[height=\iconht]{#3}}}}\xspace}

\newcommand{\doubleiconmarginraise}[3]{%
\calciconspace{#1}\calciconadj%
\reversemarginpar\marginpar{\hfill\vtop{\vskip\iconadjraise%
\hbox{\includegraphics[height=\iconht]{#2} \includegraphics[height=\iconht]{#3}}}}\xspace}

\newcommand{\tipmargin}{\iconmargin{2}{tipmargin}}
\newcommand{\tipmarginraise}{\iconmarginraise{2}{tipmargin}}
\newcommand{\infomargin}{\iconmargin{2}{notifymargin}}
\newcommand{\infomarginraise}{\iconmarginraise{2}{notifymargin}}
\newcommand{\attentionmargin}{\iconmargin{2}{warnmargin}}
\newcommand{\attentionmarginraise}{\iconmarginraise{2}{warnmargin}}
\newcommand{\dangermargin}{\iconmargin{2}{dangermargin}}
\newcommand{\dangermarginraise}{\iconmarginraise{2}{dangermargin}}

% Figures and Tables

\renewcommand{\sidecaption}{\@ifnextchar [{\@sidecaption}{\@sidecaption[]}}
\def\endsidecaption{}
\def\@sidecaption[#1]#2{%
  \@ifnextchar [{\@@sidecaption{#1}{#2}}{\@@sidecaption{#1}{#2}[]}}
\def\@@sidecaption#1#2[#3]{%
  \ifx\@empty#1\@empty
    \def\m@mscap@fortoc{#2}%
  \else
    \def\m@mscap@fortoc{#1}%
  \fi
  \ifx\@empty#1\@empty
	\caption{#2}%
  \else
    \caption[#1]{#2}%
  \fi
  \ifx\@empty#3\@empty
  \else
    \label{#3}%
  \fi}

\captionstyle{\raggedright}
\captionnamefont{\bfseries}

\newcommand{\loosertables}{\renewcommand{\arraystretch}{1.40}}
\newcommand{\loosetables}{\renewcommand{\arraystretch}{1.25}}
\loosetables

% EBNF Grammar
\newlength{\syntaxlen}
\newlength{\grammarindentlen}
\newenvironment{grammar}[2][0pt]{\setlength{\grammarindentlen}{\blockindentlen}\addtolength{\grammarindentlen}{#1}\settowidth{\syntaxlen}{#2\ }%
  \begin{em}\hspace*{\grammarindentlen}\small\begin{tabular}{@{}p{\syntaxlen}@{~}c@{~~}l}}{\end{tabular}\end{em}}%
\newcommand{\ebnf}[2]{\ifthenelse{\equal{#1}{opt}}{#2$_{\mathrm{\emph{opt}}}$}{\ifthenelse{\equal{#1}{0}}%
   {$\langle$#2$\rangle^*$}{\ifthenelse{\equal{#1}{1}}{$\langle$#2$\rangle^\textrm{\tiny{+}}$}{ERROR}}}}
\newcommand{\is}{\texttt{\em:\hspace*{-2pt}:\hspace*{-1pt}=}}
\newcommand{\choice}{\texttt{\em |}}
\newcommand{\oneof}{\textit{one of}}

% URLs
\newcommand{\linkdesc}[2]{\htmladdnormallink{#2}{#1}}
\newcommand{\xurldesc}[2]{\htmladdnormallink{\textbf{#2}}{#1}}
\newcommand{\xurl}[1]{\xurldesc{#1}{\texttt{#1}}}
\newcommand{\parurl}[1]{\par\xurl{#1}\par}

% Compatibility
\newcommand{\DocumentFooterFix}{}
\newenvironment{fullwidth}{}{}
\newcommand{\fullwidthbigindent}{\hspace*{22mm}}
\newcommand{\clearemptydoublepage}{\newpage\cleardoublepage}
\let\inthiscollection=\comment
\let\endinthiscollection=\endcomment
\let\inthisdocument=\comment
\let\endinthisdocument=\endcomment
\let\inthispart=\comment
\let\endinthispart=\endcomment
\newcommand{\windowsmargin}{\ }
\newcommand{\macmargin}{\ }
\newcommand{\linuxmargin}{\ }
\newcommand\Hline{\hline}
\newcommand\Toprule{\toprule}

% Old compatibility (during dev only)
\def\Smaller{\fontsize{7.5pt}{8.5pt}\selectfont}
\newif\ifen\entrue
\newcommand{\Y}{Y}
\newcommand{\N}{N}
\newcommand{\token}[1]{\textnormal{\texttt{#1}}}
\newcommand{\pfinalpagebreak}{}
\newcommand{\wfinalkillfooter}{}
\newcommand{\wfinalnewpage}{}


\makeatletter
\def\ScaleIfNeeded{%
  \ifdim\Gin@nat@width>\linewidth
    \linewidth
  \else
    \Gin@nat@width
  \fi
}
\makeatother

% For the sphinx generator we specify the toc at the front

\newcommand{\pretoc}{\newpage\toc}
\newcommand{\posttoc}{}


