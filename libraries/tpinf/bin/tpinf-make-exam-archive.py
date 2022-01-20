import tpinf
import sys
import os

dirname = 'exam-subject'
tpinf.workspace.create_makefile(dirname)
os.system('cp *.cpp *.hpp {}'.format(dirname))
os.system('cd {}; git init; git add *; git commit -am "initial files"'.format(dirname))



