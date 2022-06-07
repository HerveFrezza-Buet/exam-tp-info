
import sys
import os
from pathlib import Path


if len(sys.argv) != 3:
    print(f'Usage : {sys.argv[0]} <list.txt> <editor>')
    sys.exit(0)

for l in open(sys.argv[1], 'r'):
    words = l.split()
    if len(words) > 0 and words[0][0] != '#':
        dirname   = Path(words[0])
        filenames = [dirname / Path(x) for x in words[1:]]
        command = sys.argv[2]
        for filename in filenames :
            command += ' ' + str(filename)
        os.system(command)
        
