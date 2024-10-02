from setuptools import setup, find_packages

setup(
    name='project0',
    version='1.0',
    author='Balasai Srikanth Ganti',
    author_email='ganti.b@ufl.edu',
    packages=find_packages(exclude=('tests', 'docs', 'resources')),
    install_requires=[
        'pandas',
        'pypdf',
        'urllib',
        'sqlite3'
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)
