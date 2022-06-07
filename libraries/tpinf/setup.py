
import setuptools

setuptools.setup(
    name = "tpinf",
    version = "1.0",
    scripts = ['bin/tpinf-make-testable-source.py',
               'bin/tpinf-make-exam-source.py',
               'bin/tpinf-make-exam-archive.py',
               'bin/tpinf-make-subject.py',
               'bin/tpinf-make-report.py',
               'bin/tpinf-list-questions.py',
               'bin/tpinf-list-copies.py',
               'bin/tpinf-read-copies.py'],
    packages = setuptools.find_packages(),
)
