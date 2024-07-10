from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from shared.models import BaseModel
from django.utils.translation import gettext_lazy as _


class Settings(BaseModel):
    objects = models.Manager()

    contact_telegram = models.CharField(max_length=120)
    contact_phone = models.CharField(max_length=30, null=True, blank=True)
    longitude = models.BigIntegerField()
    latitude = models.BigIntegerField()
    location_text = models.TextField(_('location_text'))
    working_hours_start = models.TimeField()
    working_hours_end = models.TimeField()
    telegram_bot = models.CharField(max_length=120)

    class Meta:
        verbose_name = _('Settings')
        verbose_name_plural = _("Settings")
        db_table = 'settings'

    def __str__(self):
        return "Settings"


class Page(BaseModel):
    title = models.CharField(_('title'), max_length=250)
    slug = models.SlugField(unique=True, max_length=250)
    content = RichTextUploadingField(_('content'))

    objects = models.Manager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Page')
        verbose_name_plural = _("Pages")
        db_table = 'pages'


class GalleryPhoto(BaseModel):
    photo = models.FileField(upload_to='photos/%Y/%m/')

    objects = models.Manager()

    def __str__(self):
        return self.photo.name

    class Meta:
        verbose_name = _('Gallery Photo')
        verbose_name_plural = _('Gallery Photos')
        db_table = 'gallery_photo'
