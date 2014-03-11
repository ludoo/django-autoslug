import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-autoslug',
    version='0.5',
    packages=['autoslug'],
    include_package_data=True,
    license='BSD License',
    description='A quick hack to automate all the repetiting tasks involved in writing models that use a unique, prepopulated slug field.',
    long_description=README,
    url='https://github.com/ludoo/django-autoslug',
    author='Ludovico Magnocavallo',
    author_email='ludo@qix.it',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
