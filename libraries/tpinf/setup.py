
import setuptools

setuptools.setup(
    name = "tpinf",
    version = "1.0",
    scripts = ['bin/tpinf-make-testable-source.py',
               'bin/tpinf-make-subject-source.py'],
    packages = setuptools.find_packages(),
)
