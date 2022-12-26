from django.contrib import admin

# Register your models here.
from .models import cidadao


class CidadaoAdmin(admin.ModelAdmin):
    list_display=('nome_completo','nome_social')

admin.site.register(cidadao, CidadaoAdmin)