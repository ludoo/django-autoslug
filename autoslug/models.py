import sys

from django.core.exceptions import ValidationError
from django.db.models.base import ModelBase
from django.db.models.signals import pre_save
from django.db import models

from transliterate import transliterate


class SlugMeta(ModelBase):
    
    def __new__(cls, name, bases, attrs):
        
        if name == 'SlugBase':
            return super(SlugMeta, cls).__new__(cls, name, bases, attrs)
        
        pre_name = attrs.get('_slug_prepopulate_from')
        if not pre_name:
            raise TypeError("No valid '_slug_prepopulate_from' class attribute found")
        del attrs['_slug_prepopulate_from']
        
        pre_field = attrs.get(pre_name)
        if not pre_field:
            raise TypeError("No '%s' field found" % pre_name)
        if not isinstance(pre_field, models.CharField):
            raise TypeError("Wrong type for '%s' field" % pre_name)
        if 'slug' in attrs:
            raise TypeError("A 'slug' field already exists")

        attrs['slug'] = models.CharField(max_length=pre_field.max_length, editable=False, unique=True)
        attrs['_slug_pre'] = property(lambda s: getattr(s, pre_name))
        
        new_class = super(SlugMeta, cls).__new__(cls, name, bases, attrs)
        
        pre_save.connect(new_class._slug_pre_save, sender=new_class)
        
        return new_class
    
    
class SlugBase(models.Model):
    
    __metaclass__ = SlugMeta
    
    _slug_prepopulate_from = None # name of the field from which to prepopulate slug
    
    class Meta:
        abstract = True
        
    @staticmethod
    def _slug_transform(pre):
        return transliterate(pre or '')
    
    def _slug_update(self):
        self.slug = self._slug_transform(self._slug_pre)

    def clean(self):
        super(SlugBase, self).clean()
        value = self._slug_pre
        if not value:
            return
        self._slug_update()
        qs = type(self).objects.filter(slug=self.slug)
        if self.pk:
            qs = qs.exclude(pk=self.pk)
        if qs.count():
            raise ValidationError("Duplicate slug '%s'" % self.slug)
    
    @classmethod
    def _slug_pre_save(cls, sender, **kw):
        kw['instance']._slug_update()
        

if 'test' in sys.argv:

    class SlugTest(SlugBase):
        _slug_prepopulate_from = 'name'
        name = models.CharField(max_length=32, null=True)
