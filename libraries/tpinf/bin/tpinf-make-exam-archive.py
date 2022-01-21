import tpinf
import sys
import os

dirname = 'exam-subject'
tpinf.workspace.create_makefile(dirname)
tpinf.workspace.create_instructions()
os.system('echo type... make sign > {}/.name.cfg'.format(dirname))
os.system('cp *.cpp *.hpp {}'.format(dirname))
os.system('cd {}; git init; git add *; git commit -am "initial files"'.format(dirname))
os.system('latexmk --pdf instructions.tex')
os.system('mv instructions.pdf {}/.instructions.pdf'.format(dirname))
os.system('rm instructions.*')
os.system('tar zcvf {}.tar.gz {}; rm -rf {}'.format(dirname, dirname, dirname))
print()
print()
print()
print()
print('Archive {}.tar.gz generated.'.format(dirname))
print()


