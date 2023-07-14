from django.db import models

from ckeditor.fields import RichTextField

class PrivacyPolicy(models.Model):
    one = RichTextField(config_name='one', blank=True, null=True, default=None)
    two = RichTextField(config_name='two', blank=True, null=True, default=None)
    three = RichTextField(config_name='three', blank=True, null=True, default=None)
    text = RichTextField(blank=True, null=True, default=None)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Политика конфиденциальности'
        verbose_name_plural = 'Политики конфиденциальности'
