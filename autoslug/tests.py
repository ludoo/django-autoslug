# encoding: utf-8

import doctest


"""
>>> from django.core.exceptions import ValidationError
>>> from django.db import IntegrityError
>>> from autoslug.models import SlugTest, SlugTestNonUnique
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
>>> try: s.save()
... except IntegrityError, e: print e
column slug is not unique
>>> s = SlugTest(name='à è ò')
>>> try: s.clean()
... except ValidationError, e: print e.message
Duplicate slug 'a-e-o'
>>> s.slug
'a-e-o'
>>> s1 = SlugTestNonUnique(name='à è ò')
>>> s1.save()
>>> s2 = SlugTestNonUnique(name='à è ò')
>>> s2.save()
>>> assert s1.slug == s2.slug, (s1.slug, s2.slug)
>>>
"""


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocFileSuite('tests.py'))
    return tests
