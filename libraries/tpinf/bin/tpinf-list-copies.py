
import sys
from pathlib import Path


if len(sys.argv) < 4:
    print(f'Usage : {sys.argv[0]} <copies-dir> <list.txt> n1 n2 n3 ...')
    print(f'        nis are the part numbers of the parts which should be listed')
    sys.exit(0)

copy_dir      = Path(sys.argv[1])
list_filename = Path(sys.argv[2])
parts         = [int(x) for x in sys.argv[3:]]


copies = {}

def parse_copies(dirpath):
    hpp = list(dirpath.glob('part*.hpp'))
    cpp = list(dirpath.glob('part*.cpp'))
    if len(hpp) + len(cpp) == 0:
        for sub in dirpath.iterdir():
            if sub.is_dir():
                parse_copies(sub)
    else:
        files = []
        for n in parts :
            filename = f'part{n}.hpp'
            for p in hpp:
                if p.name == filename:
                    files.append(filename)
            filename = f'part{n}.cpp'
            for p in cpp:
                if p.name == filename:
                    files.append(filename)
        if len(files) != 0:
            copies[dirpath] = files
            
parse_copies(copy_dir)
keys = [k for k in copies.keys()]
keys.sort()

copies = {k: copies[k] for k in keys}
with open(list_filename, 'w') as list_file:
    list_file.write('# This lists the copies you have to view.\n')
    list_file.write('# Comment the next lines for the copies you\n')
    list_file.write('# have already processed.\n')
    list_file.write('\n')
    for k,v in copies.items():
        line = str(k)
        for f in v:
            line += f' {f}'
        list_file.write(line+'\n')


print()
print()
print()
print()
print(f'copy list "{list_filename}" generated.')
print()

            


