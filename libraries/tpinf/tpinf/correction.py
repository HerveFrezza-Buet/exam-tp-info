from pathlib import Path

class SameOutputDir(Exception):
    pass

class BadPragmas(Exception):
    pass

PRAMGA_OPEN_ANSWER =  'tpinf_open_answer'
PRAMGA_CLOSE_ANSWER = 'tpinf_close_answer'

PRAMGA_OPEN_ONLY_IN_SUBJECT =  'tpinf_open_only_in_subject'
PRAMGA_CLOSE_ONLY_IN_SUBJECT = 'tpinf_close_only_in_subject'

PRAGMA_Q = 'tpinf_Q'

all_unprinted_pragmas = [PRAMGA_OPEN_ANSWER,
                         PRAMGA_CLOSE_ANSWER,
                         PRAMGA_OPEN_ONLY_IN_SUBJECT,
                         PRAMGA_CLOSE_ONLY_IN_SUBJECT]

class Pragma:
    def __init__(self, start, end):
        self.in_pragma = False
        self.start = start
        self.end = end

    def __call__(self, line):
        words = line.split()
        if len(words) < 2:
            return not self.in_pragma
        if words[0] != '#pragma':
            return not self.in_pragma
        if words[1] == self.start:
            if self.in_pragma:
                raise BadPragmas
            self.in_pragma = True
            return False
        if words[1] == self.end:
            if not self.in_pragma:
                raise BadPragmas
            self.in_pragma = False
            return False
        if words[1] in all_unprinted_pragmas:
            return False
        return not self.in_pragma


def __check_files(file_in, out_dir):
    if not isinstance(file_in, Path):
        file_in = Path(file_in)
    if not isinstance(out_dir, Path):
        out_dir = Path(out_dir)
    if file_in.resolve().parent.samefile(out_dir.resolve()):
        raise SameOutputDir
    file_out = out_dir / file_in.name
    return file_in, file_out

def __remove_in_pragmas(file_in, out_dir, start, end):
    source, dest = __check_files(file_in, out_dir)
    pragma = Pragma(start, end)
    with open(dest, 'w') as out:
        for line in open(source):
            if pragma(line):
                out.write(line)
    
def remove_solution(file_in, out_dir):
    __remove_in_pragmas(file_in, out_dir, PRAMGA_OPEN_ANSWER, PRAMGA_CLOSE_ANSWER)
                
def make_testable(file_in, out_dir):
    __remove_in_pragmas(file_in, out_dir, PRAMGA_OPEN_ONLY_IN_SUBJECT, PRAMGA_CLOSE_ONLY_IN_SUBJECT)

def list_questions():
    path = Path('.')
    files = list(path.glob('*.hpp')) + list(path.glob('*.cpp'))
    all_tags = []
    res = {}
    for filename in files:
        for line in open(filename):
            words = line.split()
            if len(words) > 2 and words[0] == '#pragma' and words[1] == PRAGMA_Q:
                if len(words) < 3:
                    print(f'Error in file {filename} : pragma {PRAGMA_Q} with no tag.')
                    raise ValueError
                else:
                    tag = words[2]
                    if tag in all_tags:
                        print(f'Error in file {filename} : the tag {tag} is already used.')
                        raise ValueError
                    all_tags.append(tag)
                    if not (filename in res):
                        res[filename] = [tag]
                    else:
                        res[filename].append(tag)
    return len(all_tags), res
            
                        
