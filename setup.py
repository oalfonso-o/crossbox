import os
from setuptools import find_packages, setup
from crossbox import __version__

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

install_requires = [
    'Django',
    'django-jet',
    'pytz',
    'python-dotenv',
    'django-filter',
    'Markdown',
    'Pygments',
    'djangorestframework',
    'bcrypt',
    'psycopg2-binary',
]

tests_require = [
    'freezegun',
]

setup(
    name='oalfonso-crossbox',
    version=__version__,
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    description='Crossbox Palau',
    long_description=README,
    url='https://bitbucket.org/oalfonso_o/',
    author='Oriol Alfonso',
    author_email='oriolalfonso91@gmail.com',
    install_requires=install_requires,
    package_data={
        'crossbox': [
            'templates/*.html', 'static/*', 'static/images/*', 'static/css/*',
            'static/js/*', 'static/js/components/*', 'static/fonts/*',
            'fixtures/*',
        ],
    },
    tests_require=tests_require,
)
