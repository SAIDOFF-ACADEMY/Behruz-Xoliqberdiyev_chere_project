from modeltranslation.translator import register, TranslationOptions
from .models import Settings, Page, GalleryPhoto


@register(Settings)
class SettingsTranslationOptions(TranslationOptions):
    fields = ('location_text',)


@register(Page)
class PageTranslationOptions(TranslationOptions):
    fields = ('title', 'content',)


@register(GalleryPhoto)
class GalleryPhotoTranslationOptions(TranslationOptions):
    pass