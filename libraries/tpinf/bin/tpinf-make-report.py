import tpinf
import sys
from pathlib import Path

if len(sys.argv) != 2:
    print('Usage : {} <copies-dir>'.format(sys.argv[0]))
    sys.exit(1)

all_tags = set()
all_students = []
tpinf.marks.collect(Path(sys.argv[1]), all_tags, all_students)
all_students.sort(key = lambda x : x.name)

# A set should be sorted... I do not understant why I need this.
all_tags = list(all_tags)
all_tags.sort()

tpinf.marks.make_report(all_tags, all_students)
