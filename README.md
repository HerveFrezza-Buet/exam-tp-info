# Exam TP Info

This provides tools for setting up a programming test based on a labwork.

## Pre-installation

```
sudo apt install git make texlive-latex-base latexmk
```

## Installation

Clone this project somewhere

```
cd SOMEWHERE
git clone https://github.com/HerveFrezza-Buet/exam-tp-info.git
```

Let us call `PACKAGE_PATH` the path to the directory you have just
cloned (i.e. `SOMEWHERE/exam-tp-info`).

We have to install some python tools

```
cd PACKAGE_PATH/libraries/tpinf
python3 setup.py install --user
```

## Usage

### Principle

Define a directory (called SUBJECT here) containing your
subject. This has to contain C++ files. Questions are gathered into
parts. Indeed, a question is "make this code compile fine and execute
right".

For example, question 3 in part 2 consists in compiling some
`question3-part2.cpp` file. Naming is important, and ids of questions
and part (3 and 2 here) must be a single char. Let us denote by
`question$Q$-part$P$.cpp` this naming pattern (`$Q$` and `$P$` stands for a
single char, use letters A, B, C if you have more than 10
possibilities).

For a question to be compiled correctly, the student may need to edit
related files. In our approach, and this is what parts are, for a
given `$P$`, all questions `question$Q$-part$P$.cpp` are related to a
`part$P$.hpp` and an eventual `part$P$.cpp` file. The students fill
progressively the `part$P$.*` files as they answer the
`question$Q$-part$P$.cpp` questions, making them work one after the
others.

### Instrumentation

When you design the exam, you need to test that, once part*.hpp and
part*.cpp files are correctly filled, your question compile and
provide the result you expect. To do so, the idea it that you write
the solution of the exam in those files. Of course, when we will
generate the test material for the students, this should not appear.

We provide `#prama` stuff to instrument your code for that purpose.

```
#pragma tpinf_open_answer

The code here you want to hide to the students, i.e, the answer of the
question. Including this code makes your program compile fine and
produce the expected result.

#pragma tpinf_close_answer
```

You may also want to define code sections that appear in the test, but
that you do not want to include in your code when you test it.

```
#pragma tpinf_open_only_in_subject

The code here you want to add to the students version of the file. It
can be incomplete or partial code. When you test your exam, this will
not be included in your c++ files.

#pragma tpinf_close_only_in_subject
```

Once instrumentation is done, you can generate both versions of your
files. Let us consider directories `TESTING` and `EXAM` for putting these
two versions. From SUBJECT, you can type

```
mkdir TESTING EXAM
find . -maxdepth 1 \( -name '*.hpp' -o -name '*.cpp' \) -exec tpinf-make-testable-source.py \{} TESTING \;
find . -maxdepth 1 \( -name '*.hpp' -o -name '*.cpp' \) -exec tpinf-make-exam-source.py \{} EXAM \;
```

The above commands invoke `tpinf-make-*` filtering scripts provided by tpinf.

Within the `tpinf_open_answer... tpinf_close_answer` sections, extra
pragma can be introduced. These are tags for the corrector. It looks like

```
#pragma tpinf_Q QUESTION_TAG MARK
```

The question tag *mustn't have blank separators*, and the mark is a
number. Indeed, when the corrector annotates student code, s/he will
adds these pragmas in the student code to give a mark to the question,
so that collection of marks can be automated. Here, in the "answer"
section, writing only

```
#pragma tpinf_Q QUESTION_TAG
```

without any mark is a hint for the corrector telling which question
tag is required for that specific element of the answer.

### Overview

Once you have gathered all the code for a subject, you can overview
the question you have defined.

```
cd SUBJECT
tpinf-list-questions.py
```

This is usefull if you have built the SUBJECT content by picking several
questions from a database (see further).


### Building the test archive

The test archive is the archive you have to extract on the student
working station. You only have to execute the following commands. 

```
cd SUBJECT
tpinf-make-exam-archive.py
```

It creates a the `exam-subject.tar.gz` archive you will have to
extract at the student machines. Of course, the exam version of your
C++ files are added into the archive.

### Pick up in an exercises database

You may build up your exams every year by picking questions from a
database. Here, this strategy consists in having several directories,
each one containing a single part and the assorted questions. So there
are in such a directory: part.hpp, eventually part.cpp, and
question$Q$.cpp files including the part.hpp file.

The principle of exam generation is to build up an exam directory,
where each of the single-part directory that is to be used in the exam
is copied and re-written, since parts are associated with an actual
number. So for one of them, if it corresponds to part3 in the final
exam, you will have:

- part.hpp --> part3.hpp
- part.cpp --> part3.cpp (and the code #include "part.hpp" is re-written accordingly)
- question$Q$.cpp --> question$Q$-part3.cpp (and the code #include "part.hpp" is re-written accordingly)

Moreover, in all files, question tags are prefixed with "3-" (for part
3), and every occurrence of PART is replaced by part3 (here).

We provide you in directory `PACKAGE_PATH/fake-subject-database`
several parts, ready to be included in a specific subject. Let us use
`list` and `vector` parts as elements of this year exam. Go somewhere
you want to generated your subject. We want the vector part to be the
first part, and list part to be the second part.

```
cd where-i-gather-all-the exam-subjects
mkdir 2020-2021-c++-exam-session1
tpinf-make-subject.py 2020-2021-c++-exam-session1 PACKAGE_PATH/fake-subject-database/vectors PACKAGE_PATH/fake-subject-database/lists
```

And that's it, the directory 2020-2021-c++-exam-session1 can be used
as the SUBJECT directory mentionned previously. For example, it the
database contains subjects that have been already tested, you can
generate an exam archive like this:

```
cd 2020-2021-c++-exam-session1
tpinf-make-exam-archive.py
```

and you're done.


### Correction

There is no specific tool for the correction. Let us call COPIES the
directory containing a tree of subdirectories where the students'
directory are organized (In PACKAGE_PATH, you are given a
`PACKAGE_PATH/fake-copies` directory that can be used as COPIES for
playing with the following instructions).

First, generate the solution is some SOLUTION directory.

```
mkdir SOLUTION
cd SUBJECT
find . -maxdepth 1 \( -name '*.hpp' -o -name '*.cpp' \) -exec tpinf-make-testable-source.py \{} SOLUTION \;
```

If the writer of the subject did the things right, you should have
`#pragma tpint_Q QUESTION_TAG` lines in the files placed in
SOLUTION. The files there are very usefull for the corrector, who can
refer to them.

The easiest way is certainly to make a list of the files you have to
correct in some text file. tpinf provide tools for that.

First make the list of all the files you have to correct. Last argument is the part number (or several once), since we build the list for the correction of a specific part (or set of parts). Some correctors can thus be affected to one part, and make the file liste for it only (part 1 in the following command).

```
tpinf-list-copies.py COPIES my_list.txt 1

```

Try to edit my_list.txt, each line correponds to a bunch of files that will be opened together. As suggested, you can comment the lines for the copies you have already corrected.

Okay, let us read the copies. You can loop on the non-commented lines `my_list.txt` content in order to launch an editor (emacs here)

```
tpinf-read-copies.py my_list.txt emacs
```

Correction consists in annotating the files with comments... and give
a mark to the questions, i.e. add to the `#pragma tpint_Q QUESTION_TAG` lines
the mark (`#pragma tpint_Q QUESTION_TAG MARK`) it deserves.


### Make the exam report.

In order to gather all the marks given so far in the COPIES
directory, go into its parent directory, and type

```
tpinf-make-report.py fake-copies/
```

And you get a `.xls` file.







