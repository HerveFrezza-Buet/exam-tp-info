import tpinf
import sys

if len(sys.argv) != 3:
    print('Usage : {} code-file output-dir'.format(sys.argv[0]))
    sys.exit(1)
    
tpinf.correction.make_testable(sys.argv[1], sys.argv[2])



