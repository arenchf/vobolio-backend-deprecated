from django.contrib import admin
from .models import Dictionary

class DictionaryAdmin(admin.ModelAdmin):
    model = Dictionary


admin.site.register(Dictionary,DictionaryAdmin)
