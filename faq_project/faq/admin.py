from django.contrib import admin
from django.core.cache import cache
from .models import FAQ

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question_en',)
    fieldsets = (
        (None, {'fields': ('question_en', 'answer')}),
        ('Translations', {'fields': ('question_hi', 'question_bn')}),
    )

    def save_model(self, request, obj, form, change):
        cache.clear()
        super().save_model(request, obj, form, change)