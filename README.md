Django auto slug
================

A quick hack to automate all the repetitive tasks involved in writing models that use a unique slug field prepopulated from a CharField:

* transliterating and normalizing from text to slug
* setting the slug on model clean
* setting the slug with a pre_save receiver

To use it, simply extend SlugBase and define a `_slug_prepopulate_from` attribute in your model, with the name of the field to use for prepopulating the slug. If you need to customize slug generation, simply override `slug_transform()`.

A simple example:

```python

class SlugTest(SlugBase):
    """
    >>> s = SlugTest(name='à è ò')
    >>> s.save()
    >>> s.slug
    'a-e-o'
    >>> s = SlugTest(name='a-e     ò')
    >>> try: s.save()
    ... except IntegrityError, e: print e
    column slug is not unique
    >>> s = SlugTest(name='à è ò')
    >>> try: s.clean()
    ... except ValidationError, e: print e.message
    Duplicate slug 'a-e-o'
    >>> s.slug
    'a-e-o'
    >>>
    """
    _slug_prepopulate_from = 'name'
    _slug_field_args = {'unique':True}
    name = models.CharField(max_length=32, null=True)

```

Django Auto Slug is released under the BSD license, like Django itself.

