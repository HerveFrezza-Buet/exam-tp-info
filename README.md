# Exam TP Info

This provides tools for setting up a programming test based on a labwork.

## Pre-installation

```
sudo apt install git makefile texlive-latex-base latexmk
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
be not include in your c++ files.

#pragma tpinf_close_only_in_subject
```

Once instrumentation is done, you can generate both versions of your
files. Let us consider directory `TESTING` and `EXAM` for putting these
two versions. From SUBJECT, you can type

```
mkdir TESTING EXAM
find . -maxdepth 1 \( -name '*.hpp' -o -name '*.cpp' \) -exec tpinf-make-testable-source.py \{} TESTING \;
find . -maxdepth 1 \( -name '*.hpp' -o -name '*.cpp' \) -exec tpinf-make-subject-source.py \{} EXAM \;
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


### Building the test archive

The test archive is the archive you have to extract on the student
working station. You only have to execute the following commands.

```
cd SUBJECT
tpinf-make-exam-archive.py
```

It creates a the `exam-subject.tar.gz` archive you will have to
extract at student machines.


### Correction

There is no specific tool for the correction. Let us call COPIES the
directory containing a tree of subdirectories where the students'
directory are organized. In PACKAGE_PATH, you are given a `PACKAGE_PATH/fake-copies`
directory that can be used as COPIES for testing.

First, generate the solution is some SOLUTION directory.

```
mkdir SOLUTION
cd SUBJECT
find . -maxdepth 1 \( -name '*.hpp' -o -name '*.cpp' \) -exec tpinf-make-testable-source.py \{} SOLUTION \;
```

If the writer of the subject did the things right, you should have
`#pragma tpint_Q QUESTION_TAG` lines in the files placed in SOLUTION.

Make a list of the files you have to correct in some text file. For example

```
find COPIES -name 'part1.c=hpp' > my_list.txt
```

Then, you can loop on the `my_list.txt` content in order to launch an editor.

```
for f in $(cat my_list.txt); do echo opening $f; gedit $f; done
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







