# Exam TP Info

This provides tools for setting up a programming test based on a labwork.

## Pre-installation

```sudo apt install git makefile texlive-latex-base latexmk```

## Installation

Clone this project somewhere

```cd <somewhere>
git clone https://github.com/HerveFrezza-Buet/exam-tp-info.git
```

Let us call `<package-path>` the path to the directory you have just
cloned (i.e. `<somewhere>/exam-tp-info`).

We have to install some python tools

```cd <package-path>/libraries/tpinf
python3 setup.py install --user
```

## Usage

### Principle

Define a directory (called <subject> here) containing your
subject. This has to contain C++ files. Questions are gathered into
parts. Indeed, a question is "make this code compile fine and execute
right".

For example, question 3 in part 2 consists in compiling some
`question3-part2.cpp` file. Naming is important, and ids of questions
and part (3 and 2 here) must be a single char. Let us denote by
`question$Q$-part$P$.cpp` this naming pattern (`$Q$` and `$P$` stands for a
single char, use letters A, B, C if you have more than 10
possibilities).

For a question to be compiled correctly, the student my need to edit
related files. In our approach, and this is what parts are, for a
given `$P$`, all questions `question$Q$-part$P$.cpp` are related to a
`part$P$.hpp` and an eventual `part$P$.cpp` file. The student fill these
one or two files as they make the `question$Q$-part$P$.cpp` work.

### Instrumentation

When you design the exam, you need to test that, once part*.hpp and
part*.cpp files are correctly filled, your question compile and
provide the result you expect. To do so, the idea it that you write
the solution of the exam in those files. Of course, when we will
generate the test material for the students, this should not appear.

We provide `#prama` stuff to instrument your code for that purpose.

```
#pragma tpinf_open_answer
The code here you want to add to the students...
... i.e, the answer of the question
#pragma tpinf_close_answer
```

You may also want to define code sections that appear in the test, but
that you do not want to include in your code when you test it.

```
#pragma tpinf_open_only_in_subject
The code here you want to add to the students...
... i.e, the answer of the question
#pragma tpinf_close_only_in_subject
```

Once instrumentation is done, you can generate both versions of your
files. Let us consider directory `testing` and `exam` for putting these
two versions. From <subject>, you can type

```mkdir testing exam
find . -maxdepth 1 \( -name '*.hpp' -o -name '*.cpp' \) -exec tpinf-make-testable-source.py \{} testing \;
find . -maxdepth 1 \( -name '*.hpp' -o -name '*.cpp' \) -exec tpinf-make-subject-source.py \{} exam \;
```

The above commands invoke `tpinf-make-*` filtering scripts provided by tpinf.

Within the `tpinf_open_answer... tpinf_close_answer` sections, extra
pragma can be introduced. These are tags for the corrector. It looks like

```
#pragma tpinf_Q <question-tag> <mark>
```

The question tag *mustn't have blank separators*, and the mark is a
number. Indeed, when the corrector annotes student code, s/he will
adds these pragmas in the student code to give a mark to the question,
so that collection of marks can be automated. Here, in the "answer"
section, writing only

```
#pragma tpinf_Q <question-tag>
```

without any mark is a hint for the corrector telling which question
tag is required for that specific element of the answer.


### Building the test archive

The test archive is the archive you have to extract on the student
working station. You only have to execute the following commands.

```
cd <subject>
tpinf-make-exam-archive.py
```

It creates a `exam-subject.tar.gz` archive.


### Correction








