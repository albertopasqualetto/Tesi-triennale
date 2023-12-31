% -------------------------------------------------------------------
%  @LaTeX-class-file{
%     filename        = "DEIThesis.cls",
%     codetable       = "ISO/ASCII",
%     keywords        = "LaTeX, UniPD, Padua, Thesis, DEI",
%     docstring       = "Class for a DEI thesis."
% --------------------------------------------------------------------

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{DEIThesis}[DEI Thesis Class]

% require hyphens option before requiring url
\RequirePackage[hyphens]{url}

% -- GENERAL SETUP --

% type
\LoadClass[12pt, a4paper, oneside, openright]{book}

% page geometry
\RequirePackage[
  headheight=2cm,
  top=3.5cm,
  bottom=3.5cm,
  footskip=1.5cm,
  footnotesep=1cm,
  % twoside,
  a4paper
]{geometry}

% export in PDF/X, PDF/A, etc...
\RequirePackage{etoolbox}
\RequirePackage{colorprofiles}
\RequirePackage[a-2b,mathxmp]{pdfx}[\today]

% language, font and encodings
\RequirePackage{newpxtext,newpxmath}
\RequirePackage[T1]{fontenc}
\RequirePackage[italian]{babel}

\hyphenpenalty=600

% -- USEFUL PACKAGES --

% spacings (\onehalfsize, \doublesize)
\RequirePackage{setspace}

% indent first line of paragraph
\RequirePackage{indentfirst}

% captions
\RequirePackage{caption}
\RequirePackage{subcaption}

% links
\RequirePackage{hyperref}

% footnotes
\RequirePackage{footnote}
\RequirePackage[bottom]{footmisc}

\newcommand{\mpfootnotes}[1][1]{
  \renewcommand{\thempfootnote}{\thefootnote}
  \addtocounter{footnote}{-1}
  \addtocounter{footnote}{#1}
  \renewcommand{\footnote}{\stepcounter{footnote}\footnotetext[\value{footnote}]}
}

\interfootnotelinepenalty=10000

% mathematics
\RequirePackage{amsmath}
\RequirePackage{siunitx}

% colors
\RequirePackage{xcolor}

% graphics
\RequirePackage{graphicx}

% algoritms
\RequirePackage{algorithm}
\RequirePackage{algorithmic}

% code snippets
\RequirePackage{listings}
\RequirePackage{fancyvrb}

% plots, drawings etc...
\RequirePackage{tikz}
\usetikzlibrary{shapes.geometric, arrows.meta, positioning}

\RequirePackage[edges]{forest}

\RequirePackage{tabularx}

% references
\RequirePackage[autostyle]{csquotes}
\RequirePackage[backend=biber]{biblatex}
\renewcommand\multicitedelim{\addsemicolon\space}
\addbibresource{references.bib}



% -- DEFINITIONS --

% university
\def\university#1{\gdef\@university{#1}}

% bachelor name
\def\bachelorname#1{\gdef\@bachelorname{#1}}

% academic Year
\def\academicYear#1{\gdef\@academicYear{#1}}

% student ID
\def\studentId#1{\gdef\@studentId{#1}}

% advisor
\def\advisor#1{\gdef\@advisor{#1}}

% co-advisor (if one)
\def\coadvisor#1{\gdef\@coadvisor{#1}}
\def\coadvisorsUniversity#1{\gdef\@coadvisorsUniversity{#1}}

% university of Padova color
\definecolor{UniPDColor}{RGB}{155, 0, 20}


% -- LINKS SETUP --

% set all links to black color
\hypersetup{
  colorlinks,
  citecolor=black,
  filecolor=black,
  linkcolor=black,
  urlcolor=black
}



% -- ITEMS AND ENUMARATIONS --

% reduce spacing for items and enumerations
\let\saveditemize=\itemize
\let\savedenditemize=\enditemize
\renewenvironment{itemize}
  {\begin{spacing}{0.5}\saveditemize}
  {\savedenditemize\end{spacing}}

\let\savedenumerate=\enumerate
\let\savedendenumerate=\endenumerate
\renewenvironment{enumerate}
  {\begin{spacing}{0.5}\savedenumerate}
  {\savedendenumerate\end{spacing}}

% italic for quotes
\let\savedquote\quote
\let\endsavedquote\endquote
\renewenvironment{quote}
    {\itshape\savedquote}
    {\endsavedquote}



% -- HEADERS AND FOOTERS --

% custom headers and footers
\RequirePackage{fancyhdr}

% custom title style
\RequirePackage{titlesec}

% remove headers and footers in blank pages
\RequirePackage{scrextend}

% box for titles
\RequirePackage{adjustbox}

% style for chapters
\titleformat{\chapter}[display]
{\Huge\filleft}
{
  \minsizebox{!}{70pt}{\colorbox{UniPDColor}{\color{white} \thechapter}}
}
{1.2ex}
{}

% style for sections
\titleformat{\section}[hang]
{\Large}
{
  \colorbox{UniPDColor}{\color{white} \thesection}
}
{1ex}
{\scshape}

% style for subsections
\titleformat{\subsection}[hang]
{\large}
{
  \colorbox{UniPDColor}{\color{white} \thesubsection}
}
{1ex}
{\scshape}

% style for subsubsections
\titleformat{\subsubsection}[hang]
{\normalsize}
{}
{0ex}
{\bfseries\scshape}

% remove line headers
\renewcommand{\headrulewidth}{0ex}

% style for headers and footers
\newcommand{\setfancyhf} {
  \fancyhf{}
  \fancyhead[RO]{{\footnotesize\leftmark}}
  % \fancyhead[LE]{{\footnotesize\rightmark}}
  \fancyfoot[RE, LO]{}
  \fancyfoot[C]{\thepage}
}



% -- FRONTMATTER --

\renewcommand{\frontmatter} {
    
  % set roman page numbering
  \pagenumbering{roman}

  % set page style
  \pagestyle{fancy}

  % create cover
  \maketitle

  % reset fancy headers
  \setfancyhf

  % set head witdth
  \setlength{\headwidth}{\textwidth}

  % custom titles
  \renewcommand{\listfigurename}{Elenco delle Figure}
  \renewcommand{\listtablename}{Elenco delle Tabelle}
  \renewcommand{\listalgorithmname}{Elenco degli Algoritmi}
  \renewcommand{\lstlistlistingname}{Elenco dei Frammenti di Codice}
  \def\listacronymname{Elenco degli Acronimi}

  \def\abstractname{Abstract}
  \def\abstractnameit{Sommario}

  \renewcommand{\bibname}{Bibliografia}

  \def\acknowledgmentsname{Ringraziamenti}

  % insert dedication page
  % \dedicationpage

  % insert abstract
  \abstractpage

  % insert table of contents
  \tableofcontents
  \cleardoublepage

  % insert list of figures
  \phantomsection
  % \setcounter{page}{11}
  \addcontentsline{toc}{chapter}{\listfigurename}
  \listoffigures
  \cleardoublepage

  % insert list of tables
  \phantomsection
  % \setcounter{page}{13}
  \addcontentsline{toc}{chapter}{\listtablename}
  \listoftables
  \cleardoublepage

  % insert list of algorithms
  % \phantomsection
  % \setcounter{page}{15}
  % \addcontentsline{toc}{chapter}{\listalgorithmname}
  % \listofalgorithms

  % insert list of code snippets
  \phantomsection
  % \setcounter{page}{17}
  \addcontentsline{toc}{chapter}{\lstlistlistingname}
  \lstlistoflistings
  \cleardoublepage

  % insert list of abbreviations/acronyms
  % \setcounter{page}{19}
  \acronyms
  % \thispagestyle{empty}
  % \mbox{} % Testo vuoto per forzare la pagina bianca
  \cleardoublepage
}



% -- TITLE/COVER --

% insert watermark
\RequirePackage{watermark}

\renewcommand{\maketitle} {
  %set custom geometry
  \newgeometry{
    top=1.5cm,
    bottom=2cm,
    inner=2cm,
    outer=2cm,
    headheight=3.5cm,
    includehead,
    includefoot,
  }

  % set head witdth
  \setlength{\headwidth}{\textwidth}

  % set watermark
  \thiswatermark{
    \centering
    \put(-380,-700) {
      \includegraphics[width=1.4\linewidth]{res/unipdbg}
    }
  }

  % set academic year in footer
  \cfoot{\normalsize\textsc{Anno Accademico \\ \@academicYear}}

  % set brands in header
  \lhead{
    \includegraphics[height=3cm]{res/ltunipd}
  }
  \rhead{
    \includegraphics[height=3cm]{res/dei}
  }

  % content
  \begin{center}

    % bachelor name
    \null \vspace{\stretch{2}}
    \normalsize\textsc{
        Dipartimento di Ingegneria dell'Informazione\\
        \vspace{1ex}
        \large Corso di Laurea Triennale in \@bachelorname
    } \\

    % title
    \vspace{3ex}
    \LARGE\textbf{\@title} \\
    \vspace{\stretch{3}}

    % authors, advisors etc...
    \doublespacing

    \begin{flushleft}
      \small
      \textsc{Laureando} \hfill \textsc{Relatore} \\
      \large{\textbf{\@author}} \hfill \large{\textbf{\@advisor}} \\
      \small
      \textbf{Matricola \@studentId} \hfill \textbf{\@university} \\
      % insert co-advisor if not empty
      % \ifx\@coadvisor\empty \else
      %   \hfill \\
      %   \hfill \textsc{Correlatori} \\
      %   \hfill \large{\textbf{\@coadvisor}} \\
      %   \small
      %   \hfill \textbf{\@coadvisorsUniversity} \\
      % \fi
        \hfill \\
        \hfill \textsc{Correlatori} \\
        \hfill \large{\textbf{Dott. Alessandro Russo}} \\
        \small
        \hfill \textbf{Università degli Studi di Padova} \\
        \hfill \large{\textbf{Dott. Matteo Spanio}} \\
        \small
        \hfill \textbf{Audio Innova} \\
    \end{flushleft}

    \vspace{\stretch{1}} \null
  \end{center}

  % restore defaults
  \cleardoublepage
  \restoregeometry
  \onehalfspacing
}



% -- DEDICATION --

\newcommand{\dedicationpage} {
  % set empty style for this page (no headers and footers)
  \thispagestyle{empty}

  \phantomsection
  
  \null \vspace{\stretch{1}}

  \begin{flushright}
    \input{frontmatter/dedication}
  \end{flushright}

  \vspace{\stretch{4}} \null
  
  % insert pages for alignment
  \cleardoublepage
}



% -- ACRONYMS/ABBREVIATIONS --

\RequirePackage{acronym}

% custom style for acronyms
\newcommand{\acronyms}{
  \phantomsection
  \addcontentsline{toc}{chapter}{\listacronymname}
  \chapter*{\listacronymname}
  \input{frontmatter/glossary}
  \cleardoublepage

  \acresetall
}



% -- ABSTRACT --

\newenvironment{abstract}[1][en] {
  % get argument (en/it)
  \def\it{it}
  \def\arg{#1}

  \null \vfill
  \begin{center}
    \bfseries
    
    % set title in english or italian
    \ifx\arg\it
      \abstractnameit
    \else
      \abstractname
    \fi
  \end{center}
} {
  \vfill \null
}

\newcommand{\abstractpage} {
  % set empty style for this page (no headers and footers)

  % english version
  % \thispagestyle{empty}
  % \input{frontmatter/abstract}
  
  % italian version
  \cleardoublepage
  \thispagestyle{empty}
  \input{frontmatter/sommario}
}



% -- MAIN MATTER --

\renewcommand{\mainmatter} {
  \cleardoublepage

  % reset page counter
  \setcounter{page}{1}

  % set arabic page numbering
  \pagenumbering{arabic}

  % reset chapter counter
  \setcounter{chapter}{0}
}



% -- BACKMATTER --

\renewcommand{\backmatter}{
  \cleardoublepage
  \phantomsection

  % add references
  \addcontentsline{toc}{chapter}{\bibname}
  \printbibliography
  
  \cleardoublepage
  \phantomsection

  % add acknowledgments
  \addcontentsline{toc}{chapter}{\acknowledgmentsname}
  \acknowledgments
}



% -- ACKNOWLEDGMENTS --
\newcommand{\acknowledgments} {
  \phantomsection
  \chapter*{\acknowledgmentsname}
  \input{frontmatter/thanks}
}


% -- CODE SNIPPETS --

\VerbatimFootnotes

\renewcommand{\lstlistingname}{Codice} % Caption name of code snippets
\renewcommand{\lstlistlistingname}{Codici}

% Colors for code snippets highlights
\definecolor{commentsColor}{RGB}{76, 113, 148}
\definecolor{numColor}{RGB}{160, 175, 132}
\definecolor{stringColor}{RGB}{205, 63, 62}
\definecolor{kwColor}{RGB}{71, 133, 126}
% \definecolor{bgCodeColor}{RGB}{255, 249, 249}

% Style of code snippets
\lstdefinestyle{codeSnippet} {
  % backgroundcolor=\color{bgCodeColor},
  commentstyle=\color{commentsColor},
  keywordstyle=\color{kwColor},
  numberstyle=\tiny\color{numColor},
  stringstyle=\color{stringColor},
  basicstyle=\ttfamily\footnotesize,
  breakatwhitespace=false,         
  breaklines=true,                 
  captionpos=b,                    
  keepspaces=true,                 
  numbers=left,                    
  numbersep=5pt,                  
  showspaces=false,                
  showstringspaces=false,
  showtabs=false,                  
  tabsize=2
}

\lstset{style=codeSnippet}


\definecolor{diffstart}{RGB}{128, 128, 128}
\definecolor{diffincl}{RGB}{64, 119, 113}
\definecolor{diffrem}{RGB}{205, 63, 62}
% \definecolor{diffincl}{RGB}{0, 128, 0}
% \definecolor{diffrem}{RGB}{255, 0, 0}

\lstdefinelanguage{diff}{
    basicstyle=\linespread{0.95}\ttfamily\footnotesize,
    morecomment=[f][\color{diffstart}]{@@},
    morecomment=[f][\color{diffincl}]{+\ },
    morecomment=[f][\color{diffrem}]{-\ },
}


\definecolor{jsondelim}{RGB}{20, 142, 193}
\definecolor{jsonnum}{RGB}{92, 51, 154}
\definecolor{jsonstring}{RGB}{163, 20, 20}
\definecolor{jsoncomment}{RGB}{169, 169, 169}

\lstdefinelanguage{json}{
    basicstyle=\linespread{0.95}\ttfamily\footnotesize,
    numbers=left,
    numberstyle=\scriptsize,
    stepnumber=1,
    numbersep=8pt,
    showstringspaces=false,
    breaklines=true,
    commentstyle=\color{jsoncomment},
    keywordstyle=\color{jsonnum},
    keywords={null,true,false},
    morestring=[b]",
    stringstyle=\color{jsonstring},
    morecomment=[l]{//},
    morecomment=[s]{/*}{*/},
    literate=
        *{0}{{{\color{jsonnum}0}}}{1}
        {1}{{{\color{jsonnum}1}}}{1}
        {2}{{{\color{jsonnum}2}}}{1}
        {3}{{{\color{jsonnum}3}}}{1}
        {4}{{{\color{jsonnum}4}}}{1}
        {5}{{{\color{jsonnum}5}}}{1}
        {6}{{{\color{jsonnum}6}}}{1}
        {7}{{{\color{jsonnum}7}}}{1}
        {8}{{{\color{jsonnum}8}}}{1}
        {9}{{{\color{jsonnum}9}}}{1}
        {\{}{{{\color{jsondelim}{\{}}}}{1}
        {\}}{{{\color{jsondelim}{\}}}}}{1}
        {[}{{{\color{jsondelim}{[}}}}{1}
        {]}{{{\color{jsondelim}{]}}}}{1},
}


% -- FILE TREES --

% Style of file trees
\definecolor{folderbg}{RGB}{107, 144, 179}
\definecolor{folderborder}{RGB}{76, 113, 148}

\newlength\Size
\setlength\Size{4pt}

\tikzset{
    folder/.pic={
        \filldraw [draw=folderborder, top color=folderbg!50, bottom color=folderbg] (-1.05*\Size,0.2\Size+5pt) rectangle ++(.75*\Size,-0.2\Size-5pt);
        \filldraw [draw=folderborder, top color=folderbg!50, bottom color=folderbg] (-1.15*\Size,-\Size) rectangle (1.15*\Size,\Size);
    },
    file/.pic={
        \filldraw [draw=folderborder, top color=folderbg!5, bottom color=folderbg!10] (-\Size,.4*\Size+5pt) coordinate (a) |- (\Size,-1.2*\Size) coordinate (b) -- ++(0,1.6*\Size) coordinate (c) -- ++(-5pt,5pt) coordinate (d) -- cycle (d) |- (c) ;
    },
    multifiles/.pic={
        \filldraw [draw=folderborder, top color=folderbg!5, bottom color=folderbg!10, shift={(-\Size*0.5, \Size*0.5)}] (-\Size,.4*\Size+5pt) coordinate (a) |- (\Size,-1.2*\Size) coordinate (b) -- ++(0,1.6*\Size) coordinate (c) -- ++(-5pt,5pt) coordinate (d) -- cycle (d) |- (c) ;
        \filldraw [draw=folderborder, top color=folderbg!5, bottom color=folderbg!10] (-\Size,.4*\Size+5pt) coordinate (a) |- (\Size,-1.2*\Size) coordinate (b) -- ++(0,1.6*\Size) coordinate (c) -- ++(-5pt,5pt) coordinate (d) -- cycle (d) |- (c) ;
        \filldraw [draw=folderborder, top color=folderbg!5, bottom color=folderbg!10, shift={(\Size*0.5, -\Size*0.5)}] (-\Size,.4*\Size+5pt) coordinate (a) |- (\Size,-1.2*\Size) coordinate (b) -- ++(0,1.6*\Size) coordinate (c) -- ++(-5pt,5pt) coordinate (d) -- cycle (d) |- (c) ;
    },
}
\forestset{
    declare autowrapped toks={pic me}{},
    pic dir tree/.style={
        for tree={
            folder,
            font=\footnotesize\ttfamily,
            grow'=0,
        },
        before typesetting nodes={
            for tree={
                edge label+/.option={pic me},
            },
        },
    },
    pic me set/.code n args=2{
        \forestset{
            #1/.style={
                inner xsep=2\Size,
                pic me={pic {#2}},
            }
        }
    },
    pic me set={directory}{folder},
    pic me set={file}{file},
    pic me set={multifiles}{multifiles},
}
