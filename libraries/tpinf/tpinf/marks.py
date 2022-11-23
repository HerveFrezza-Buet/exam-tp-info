from pathlib import Path
import xlsxwriter
from . import correction

class NameInSubdir(Exception):
    pass

class QuestionCorrectedTwice(Exception):
    pass

class OrphanCppFiles(Exception):
    pass

class Report:
    def __init__(self, path, name, all_tags):
        self.path = path
        self.name = name
        self.marks = {}
        self.all_tags = all_tags

    def inspect_line(self, line):
        words = line.split()
        if len(words) < 4:
            return
        if words[0] != '#pragma':
            return
        if words[1] != correction.PRAGMA_Q:
            return
        question_tag, mark = words[2], float(words[3])
                
        if question_tag in self.marks:
            print()
            print()
            print('For the student in {} : Found tag {} twice.'.format(self.path, question_tag))
            print()
            print()
            raise QuestionCorrectedTwice

        self.all_tags.add(question_tag)
        self.marks[question_tag] = mark
        
    def inspect_source(self, path):
        with open(path) as code:
            for line in code:
                self.inspect_line(line)


def collect(path, all_tags, all_students, student = None):
    if not isinstance(path, Path):
        path = Path(path)
    name_path = path / '.name.cfg'
    if name_path.exists():
        if student:
            raise NameInSubdir
        student_name = '???'
        with open(name_path) as name_file:
            lines = [' '.join(line.split()) for line in name_file]
            for line in lines:
                if line != '':
                    student_name = line
                    break
            student = Report(path, student_name, all_tags)
            all_students.append(student)

    files = list(path.glob('*.hpp')) + list(path.glob('*.cpp')) + list(path.glob('*.hh')) + list(path.glob('*.cc')) + list(path.glob('*.h')) + list(path.glob('*.c'))
    if student == None and len(files) > 0:
        print()
        print()
        print('Orphan c++ files found (i.e. c++ files not related to a student)')
        print('These are the following ones')
        print([str(f) for f in files])
        print()
        print()
        raise OrphanCppFiles
        
    for f in files:
        student.inspect_source(f)
        
    for subdir in path.iterdir():
        if subdir.is_dir():
            collect(subdir, all_tags, all_students, student)
            
            

def make_report(all_tags, all_students):
    workbook  = xlsxwriter.Workbook('exam-report.xlsx')
    worksheet = workbook.add_worksheet('Marks')
    formats = {'header': workbook.add_format({'bg_color' : '#eeeeee', 'bold' : True, 'align' : 'center'}),
               'path'  : workbook.add_format({'align' : 'left'}),
               'name'  : workbook.add_format({'bg_color' : '#555555', 'color' : '#ffffff', 'bold' : True, 'align' : 'left'}),
               'mark'  : workbook.add_format({'num_format' : '0.0', 'align' : 'right'}),
               'sum'  : workbook.add_format({'num_format' : '0.0', 'bold' : True, 'align' : 'right'})}
    col_path = 1
    col_name = col_path+1
    col_first_mark = col_name + 1
    col_marks = {mark : col+col_first_mark for col, mark in enumerate(all_tags)}
    col_last_mark = col_first_mark + len(col_marks) - 1
    col_sum = col_first_mark + len(col_marks) + 1
    line = 2
    
    for m, c in col_marks.items():
        worksheet.write(line, c, m, formats['header'])
    worksheet.write(line, col_sum, 'Total', formats['header'])
    line += 1

    for marks in all_students:
        worksheet.write(line, col_path, str(marks.path), formats['path'])
        worksheet.write(line, col_name, marks.name,      formats['name'])
        for tag, mark in marks.marks.items():
            worksheet.write(line, col_marks[tag], mark,  formats['mark'])
        formula = '=SUM({})'.format(xlsxwriter.utility.xl_range(line, col_first_mark, line, col_last_mark))
        worksheet.write_formula(line, col_sum, formula,  formats['sum'])
        line += 1


    workbook.close()
