from django.contrib import admin
from . models import Batch
@admin.register(Batch)
class FilmAdmin(admin.ModelAdmin):
    list_display = ['id', 'plik']