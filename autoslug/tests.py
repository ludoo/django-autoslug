# encoding: utf-8

import unittest
import doctest

"""
>>> from django.core.exceptions import ValidationError
>>> from django.db import IntegrityError
>>> from autoslug.models import SlugTest
>>> 
>>> s = SlugTest(name='First test')
>>> repr(s)
'<SlugTest: SlugTest object>'
>>> s.save()
>>> s.slug
'first-test'
>>> s = SlugTest(name='à è ò')
>>> s.save()
>>> s.slug
'a-e-o'
>>> s = SlugTest(name='a      e ò')
>>> try:
...     s.save()
... except IntegrityError, e:
...     print e
column slug is not unique
>>> s = SlugTest(name='à è ò')
>>> try: s.clean()
... except ValidationError, e: print e.message
Duplicate slug 'a-e-o'
>>> s.slug
'a-e-o'
>>> 
"""


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocFileSuite('tests.py'))
    return tests
