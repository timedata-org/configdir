from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import sys


# From here: http://pytest.org/2.2.4/goodpractises.html
class RunTests(TestCommand):
    DIRECTORY = 'test'

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = [self.DIRECTORY]
        self.test_suite = True

    def run_tests(self):
        # Import here, because outside the eggs aren't loaded.
        import pytest
        errno = pytest.main(self.test_args)
        if errno:
            raise SystemExit(errno)


class RunCoverage(RunTests):
    def run_tests(self):
        import coverage
        cov = coverage.Coverage(config_file=True)

        cov.start()
        super().run_tests()
        cov.stop()

        cov.report(file=sys.stdout)
        coverage = cov.html_report(directory='htmlcov')
        fail_under = cov.get_option('report:fail_under')
        if coverage < fail_under:
            print('ERROR: coverage %.2f%% was less than fail_under=%s%%' % (
                  coverage, fail_under))
            raise SystemExit(1)


setup(
    name='cfgs',
    version=open('VERSION').read().strip(),
    description=(
        'cfgs is a pure Python library for data and config files which '
        'implements the XDG standard for persistent files'),
    long_description=open('README.md').read(),
    author='Tom Ritchford',
    author_email='tom@swirly.com',
    url='http://github.com/timedata-org/cfgs/',
    license='MIT',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    tests_require=['pytest'],
    cmdclass={
        'coverage': RunCoverage,
        'test': RunTests,
    },
)