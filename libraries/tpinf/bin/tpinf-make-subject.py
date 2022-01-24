import tpinf
import sys
from pathlib import Path

if len(sys.argv) < 3:
    print('Usage : {} output-dir part1_dir part2_dir part3_dir...'.format(sys.argv[0]))
    sys.exit(1)

dest_dir = Path(sys.argv[1])
parts = {tpinf.workspace.LICITE_PART_TAGS[i]: Path(name) for i, name in enumerate(sys.argv[2:])}

for part, path in parts.items():
    source_files = list(path.glob('*.cpp')) +  list(path.glob('*.hpp'))
    for source_file in source_files:
        tpinf.workspace.rewrite_as_part(source_file, dest_dir, part)

print()
print()
print('Subject has been generated in {}.'.format(dest_dir.resolve()))
print()


    



