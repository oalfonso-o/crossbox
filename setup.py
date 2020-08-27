import os
from setuptools import find_packages, setup
from crossbox import __version__

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


def read_requirements(filename):
    with open(filename) as f:
        reqs = f.readlines()
    return [r.strip() for r in reqs
            if r[0] != '#' and r[:4] != 'git+' and r[:2] != '-r']


install_requires = read_requirements('./requirements.txt')

setup(
    name='oalfonso-crossbox',
    version=__version__,
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    description='Crossbox Palau',
    long_description=README,
    url='https://github.com/oalfonso-o/',
    author='Oriol Alfonso',
    author_email='oriolalfonso91@gmail.com',
    install_requires=install_requires,
    package_data={
        'crossbox': [
            'templates/*.html', 'templates/registration/*.html', 'static/*',
            'static/images/*', 'static/css/*', 'static/js/*',
            'static/js/lib/*', 'static/js/components/*', 'static/js/custom/*',
            'static/fonts/*', 'static/webfonts/*', 'fixtures/*'
        ],
    },
)
