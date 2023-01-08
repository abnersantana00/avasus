from django.contrib import admin

# Register your models here.
from .models import CustomUser, Categoria, Subforum, Topico , Resposta, VinculoSubforum


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('cpf','nome_completo', 'perfil')

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id','nome')

class SubforumAdmin(admin.ModelAdmin):
    list_display = ('cod_subforum','titulo', 'descricao', 'nome_autor')

class TopicoAdmin(admin.ModelAdmin):
    list_display = ('cod_subforum','nome_autor', 'titulo', 'descricao',)

class RespostaAdmin(admin.ModelAdmin):
    list_display = ('cod_topico','nome_autor', 'texto', 'data_criacao')

class VinculoSubforumAdmin(admin.ModelAdmin):
    list_display  = ('aluno', 'cod_subforum')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Subforum, SubforumAdmin)
admin.site.register(Topico, TopicoAdmin)
admin.site.register(Resposta, RespostaAdmin)
admin.site.register(VinculoSubforum, VinculoSubforumAdmin)

