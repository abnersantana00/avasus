from django.contrib import admin

# Register your models here.
from .models import CustomUser, Categoria, Subforum, Topico

admin.site.register(CustomUser)
admin.site.register(Categoria)
admin.site.register(Subforum)
admin.site.register(Topico)