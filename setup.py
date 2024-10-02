from setuptools import setup, find_packages

setup(
	name='assignment0',
	version='1.0',
    author='Balasai Srikanth Ganti',
    author_email='ganti.b@ufl.edu',
	packages=find_packages(exclude=('tests', 'docs', 'resources')),
	setup_requires=['pytest-runner'],
	tests_require=['pytest']	
)
