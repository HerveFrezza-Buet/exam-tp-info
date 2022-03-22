from pathlib import Path
from . import correction

class BadPartTag(Exception):
    pass

class NotCpp(Exception):
    pass

class BadQuestionFileName(Exception):
    pass

def create_makefile(dirname):

    subject_dir = Path('.') / dirname
    try:
        subject_dir.mkdir()
    except FileExistsError:
        pass
    
    part_c = sorted([f.name[4] for f in Path('.').glob('part*.cpp')])

    q = [(f.name[8], f.name[14]) for f in Path('.').glob('question*-part*.cpp')]
    toc = {part:[] for part in sorted([item[1] for item in q])}
    for question, part in q:
        toc[part].append(question)
    for p in toc.keys():
        toc[p].sort()
        
    with open(subject_dir/ 'makefile', 'w') as makefile:
        makefile.write('# generated by tpinf\n\n')
        makefile.write('GIT_CONFIG = $(HOME)/.gitconfig\n')
        makefile.write('\n')
        makefile.write('help:\n')
        makefile.write('\t@ls $(GIT_CONFIG) >/dev/null 2>/dev/null || bash -c "echo -e \'[user]\\n\\tname=Examinator\\n\\temail = examinator@centralesupelec.fr\\n\' > $(GIT_CONFIG)"\n')
        makefile.write('\t@echo\n')
        makefile.write('\t@echo\n')
        makefile.write('\t@echo "Your name:\\033[1;30m" `cat .name.cfg` "\\033[0m"\n')
        makefile.write('\t@echo "---------"\n')
        makefile.write('\t@echo\n')
        makefile.write('\t@echo\n')
        makefile.write('\t@echo "Type the following commands in order to pass the exam."\n')
        makefile.write('\t@echo "You can use the <tab> key (symbol \'->|\' on the keyboard) "\n')
        makefile.write('\t@echo "to complement a command. For example, if you type"\n')
        makefile.write('\t@echo "\\033[1;33mmake in\\033[0m "\n')
        makefile.write('\t@echo "with \\033[1;30mno return key\\033[0m and then you press the <tab> key,"\n')
        makefile.write('\t@echo "you will get the command"\n')
        makefile.write('\t@echo "\\033[1;33mmake instructions\\033[0m"\n')
        makefile.write('\t@echo "fully written automatically, ready to be executed."\n')
        makefile.write('\t@echo\n')
        makefile.write('\t@echo "------------------------------"\n')
        makefile.write('\t@echo\n')
        makefile.write('\t@echo "\\033[1;30mmake sign             \\033[0m <- Tell us your name."\n')
        makefile.write('\t@echo "\\033[1;30mmake instructions     \\033[0m <- displays the instructions."\n')
        makefile.write('\t@echo "\\033[1;30mmake oops             \\033[0m <- \\033[0;31mcall this if you delete a file accidentally.\\033[0m"\n')
        makefile.write('\t@echo\n')
        makefile.write('\t@echo "------------------------------"\n')
        makefile.write('\t@echo\n')
        for part, questions in toc.items():
            for question in questions:
                makefile.write('\t@echo "\\033[1;30mmake question{}-part{}  \\033[0m <- compiles and executes question {} of part {}."\n'.format(question, part, question, part))
            makefile.write('\t@echo\n')
        makefile.write('\t@echo "------------------------------"\n')
        makefile.write('\t@echo\n')
        makefile.write('\t@echo "Compiling \\033[1;31mmust not have warnings !!!\\033[0m"\n')
        makefile.write('\t@echo\n')
        makefile.write('\t@echo\n')
        makefile.write('\t@echo\n')
        makefile.write('\n')
        makefile.write('oops:\n')
        makefile.write('\t@echo\n')
        makefile.write('\t@echo "You need to recover a deleted file? Do not panic, this is the solution."\n')
        makefile.write('\t@echo "Follow the following steps (type \\033[1;30mmake oops\\033[0m in order to view"\n')
        makefile.write('\t@echo "this message  again):"\n')
        makefile.write('\t@echo "- Step 1 : \\033[1;30mmake show-history\\033[0m            <-- identify the commit \\033[1;30mid\\033[0m of the commit where"\n')
        makefile.write('\t@echo "                                            your file is (the first code of a line)"\n')
        makefile.write('\t@echo "- Step 2 : \\033[1;30mmake recover ID=... FILE=...\\033[0m <-- Tell the commit \\033[1;30mid\\033[0m and the file name and you"\n')
        makefile.write('\t@echo "                                            will get it back."\n')
        makefile.write('\t@echo "      e.g. \\033[1;30mmake recover ID=34b9dfd FILE=part1.hpp\\033[0m"\n')
        makefile.write('\t@echo "- Step 3 : be sure that your editor notices the file change."\n')
        makefile.write('\t@echo\n')
        makefile.write('\t@echo\n')
        makefile.write('\n')
        makefile.write('show-history:\n')
        makefile.write('\t@git log --oneline\n')
        makefile.write('\n')
        makefile.write('recover:\n')
        makefile.write('\t@git checkout $(ID) -- $(FILE) && echo file $(FILE) has been recovered.\n')
        makefile.write('\n')
        makefile.write('sign:\n')
        makefile.write('\t@echo\n')
        makefile.write('\t@echo\n')
        makefile.write('\t@read -p "enter your name (format : LAST-NAME first-name, ex: EINSTEIN Albert): " identity; echo $$identity > .name.cfg\n')
        makefile.write('\t@echo\n')
        makefile.write('\n')
        makefile.write('\n')
        makefile.write('CFLAGS = -Wall -pedantic -std=c++17\n')
        makefile.write('\n')
        makefile.write('instructions:\n')
        makefile.write('\t@evince .instructions.pdf &\n')
        makefile.write('\n')
        makefile.write('stamp: TIME = `date +"%H:%M:%S"`\n')
        makefile.write('stamp:\n')
        makefile.write('\t@rm -f test\n')
        makefile.write('\t@git commit -am "compiling of part $(PART), question $(QUESTION) : at $(TIME)" > /dev/null || true\n')
        makefile.write('\n')
        makefile.write('run:\n')
        makefile.write('\t@echo\n')
        makefile.write('\t@echo\n')
        makefile.write('\t@echo "\\033[1;32mrunning program\\033[0m..."\n')
        makefile.write('\t@echo\n')
        makefile.write('\t@./test\n')
        makefile.write('\n')
        makefile.write('\n')
        makefile.write('\n')
        makefile.write('\n')
        for part, questions in toc.items():
            for question in questions:
                target = 'question{}-part{}'.format(question, part)
                files = []
                if part in part_c:
                    files.append('part{}.cpp'.format(part))
                files.append(target + '.cpp')
                files = ' '.join(files)
                makefile.write('.PHONY: {}\n'.format(target))
                makefile.write('{}:\n'.format(target))
                makefile.write('\t@make --quiet stamp PART={} QUESTION={}\n'.format(part, question))
                makefile.write('\tg++ -o test $(CFLAGS) {}\n'.format(files))
                makefile.write('\t@make --quiet run\n')
                makefile.write('\n')



def create_instructions():
    with open('instructions.tex', 'w') as latex :
        latex.write("\\documentclass[a4paper,10pt]{article}\n")
        latex.write("\n")
        latex.write("\\usepackage[utf8]{inputenc}\n")
        latex.write("\\usepackage[margin=2cm]{geometry}\n")
        latex.write("\\usepackage[colorlinks=true, linkcolor=blue, anchorcolor=blue,\n")
        latex.write("citecolor=blue, filecolor=blue, menucolor=blue,\n")
        latex.write("urlcolor=blue]{hyperref}\n")
        latex.write("\n")
        latex.write("\\setlength{\\parskip}{3mm}\n")
        latex.write("\\setlength{\\parindent}{0mm}\n")
        latex.write("\n")
        latex.write("\\begin{document}\n")
        latex.write("\\centerline{\\Large \\sc Instructions for the test}\n")
        latex.write("\\vspace{5mm}\n")
        latex.write("\\hrule\n")
        latex.write("\\vspace{5mm}\n")
        latex.write("\\tableofcontents\n")
        latex.write("\n")
        latex.write("\\section{Getting started}\n")
        latex.write("\n")
        latex.write("We consider in the followwing that you have opened a terminal, and that you are placed in the directory where the exam materials lies.\n")
        latex.write("\n")
        latex.write("In that terminal, typing only\n")
        latex.write("\\begin{verbatim}make\n")
        latex.write("\\end{verbatim}\n")
        latex.write("helps you. It displays help. Read the forewords displayed by this command.\n")
        latex.write("\n")
        latex.write("\\begin{verbatim}make sign\n")
        latex.write("\\end{verbatim}\n")
        latex.write("and check that your name is correct (read the first line displayed)\n")
        latex.write("The first thing to do is register your name. Type the following\n")
        latex.write("\\begin{verbatim}make\n")
        latex.write("\\end{verbatim}\n")
        latex.write("\n")
        latex.write("\\section{How to pass the test}\n")
        latex.write("\n")
        latex.write("The exam is organized into parts. In each part, there are several questions, that have to be considered in order.\n")
        latex.write("\n")
        latex.write("For part~1 (the same stands for part 2, 3, ...) you are given the following {\\tt C++} files. {\\bf Just read the following}, you will have to really do something at section~\\ref{sec:starting}.\n")
        latex.write("\\begin{itemize}\n")
        latex.write("  \\item {\\tt part1.hpp}: This is where you will have to write code when you will be asked to do so.\n")
        latex.write("  \\item {\\tt part1.cpp}: May not be present. If it exists, you will be asked to write code in it as well.\n")
        latex.write("  \\item {\\tt question1-part1.cpp}: This file contains the instructions corresponding to first question of part~1. {\\bf Do not modify this file}\\footnote{Except if you are explicitly told to do so.}. Read it, comments will tell you what to do, where to write code, etc. If you do things right, compiling {\\tt question1-part1.cpp} should succeed and it will output what is expected.\n")
        latex.write("  \\item {\\tt question2-part1.cpp}: Next question...\n")
        latex.write("  \\item {\\tt question3-part1.cpp}: Next question...\n")
        latex.write("  \\item {\\tt ...}\n")
        latex.write("\\end{itemize}\n")
        latex.write("\n")
        latex.write("Once you have implemented what is required by, let us say, {\\tt question3-part2.cpp}, you have to compile the {\\tt question3-part2.cpp} and run the resulting program. {\\bf Do not invoke g++ directly}, we provide you with this simplified command.\n")
        latex.write("\\begin{verbatim}make question3-part2\n")
        latex.write("\\end{verbatim}\n")
        latex.write("\n")
        latex.write("You will not have to type everything if you use the completion key (the {\\tt TAB} key).\n")
        latex.write("\n")
        latex.write("In case of compiling errors, output that not fit the requirements, you will have to modify your code (in {\\tt part2.hpp} or {\\tt part2.cpp} in this example), and retry the command until everything succeeds. \n")
        latex.write("\n")
        latex.write("\\section{Start the test \\label{sec:starting}}\n")
        latex.write("\n")
        latex.write("Now, type\n")
        latex.write("\n")
        latex.write("\\begin{verbatim}make\n")
        latex.write("\\end{verbatim}\n")
        latex.write("\n")
        latex.write("to display all the questions (lines like {\\tt make question-X-part-Y}). Edit the {\\tt c++} file corresponding to the question you address with one of the available code editors. This file is {\\tt question-X-part-Y.cpp} if you have typed {\\tt make question-X-part-Y}. Reading the comments tells you what to do (don't modify that file if you are not explicitly asked to). Compile and test that question by typing the corresponding \n")
        latex.write("\n")
        latex.write("\\begin{verbatim}make questionX-partY\n")
        latex.write("\\end{verbatim}\n")
        latex.write("\n")
        latex.write("command.\n")
        latex.write("\n")
        latex.write("\\section{Warnings}\n")
        latex.write("\n")
        latex.write("The documentation is available on this machine, you have no access to internet, and no extra electronic devices are allowed.\n")
        latex.write("\n")
        latex.write("{\\bf DO NOT} access collections elements with the {\\tt []} operator, like in {\\tt  tab[4]}, since this is not efficient within loops.\n")
        latex.write("\n")
        latex.write("Each function you will have to implement {\\bf is short} (less than 10 lines). Do not get lost in obfuscated code !\n")
        latex.write("\n")
        latex.write("Be sure to save the files you have modified before the end of the test. Do not create new files, anwsering consists in modifying the given files.\n")
        latex.write("\n")
        latex.write("Use {\\tt make oops} in case of accidental file deletions... but the best is to avoid it.\n")
        latex.write("\n")
        latex.write("\n")
        latex.write("\n")
        latex.write("\\end{document}\n")
        
LICITE_PART_TAGS = [str(i) for i in range(1, 10)] + [chr(i+65) for i in range(26)]

def __rewrite_filename(source_name, part):
    partname = 'part{}'.format(part)
    if source_name == 'part.cpp':
        return partname + '.cpp'
    elif source_name == 'part.hpp':
        return partname + '.hpp'
    elif len(source_name) < 13:
        raise BadQuestionFileName
    elif source_name[:8] != 'question':
        raise BadQuestionFileName
    elif source_name[9:] != '.cpp':
        raise BadQuestionFileName
    elif source_name[8] not in LICITE_PART_TAGS:
        raise BadQuestionFileName
    return 'question' + source_name[8] + '-part{}.cpp'.format(part)

def __rewrite_line(line, part):
    res = line.replace('part.hpp', 'part{}.hpp'.format(part))
    res = res.replace('part.cpp', 'part{}.cpp'.format(part))
    res = res.replace('PART', 'part{}'.format(part))
    words = line.split()
    if len(words) > 2:
        if (words[0], words[1]) == ('#pragma', correction.PRAGMA_Q):
            words[2] = '{}-'.format(part)+ words[2]
            res = ' '.join(words)+'\n'
    return res
    
def rewrite_as_part(source_file, dirname, part):
    if not isinstance(part, str):
        raise BadPartTag
    if len(part) != 1:
        raise BadPartTag

    if not isinstance(source_file, Path):
        source_file = Path(source_file)
        
    if not isinstance(dirname, Path):
        dirname = Path(dirname)

    if source_file.suffix not in ['.cpp', '.hpp']:
        raise NotCpp
    
    dest_file = dirname / __rewrite_filename(source_file.name, part)

    with open(dest_file, 'w') as dest:
        for line in open(source_file):
            dest.write(__rewrite_line(line, part))
