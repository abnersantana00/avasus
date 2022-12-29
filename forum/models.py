from django.db import models
from .manager import *
# Create your models here.
from django.contrib.auth.models import AbstractUser
from datetime import date

class CustomUser(AbstractUser):
    username = None
    nome_completo = models.CharField(max_length=60, default=' ')
    nome_social = models.CharField(max_length=50, default=' ')
    cpf = models.CharField(unique=True, max_length=11)
    nasc = models.DateField(default=date.today())
    estado = models.CharField(max_length=2, default=' ')
    cidade = models.CharField(max_length=50, default=' ')
    TIPO_USUARIO = (
        ("PROF", "Professor"),
        ("ALU", "Aluno"),
    )
    perfil = models.CharField(choices=TIPO_USUARIO, max_length=4, default='ALU')
    objects = UserManager()
    USERNAME_FIELD = 'cpf'
    REQUIRED_FIELDS = []

class Categoria(models.Model):
    id = models.IntegerField(primary_key=True)
    nome = models.IntegerField(max_length=45, default=" ")

class Subforum(models.Model):
    cod_subforum = models.AutoField(primary_key=True)
    autor = autor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    cat_subforum = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=120, default=' ')
    descricao = models.CharField(max_length=512, default=' ')
    data_criacao = models.DateField(default=date.today())
    ESTADO = (
        ("ATV", "Ativado"),
        ("TRC", "Trancado"),
    )
    estado = models.CharField(choices=ESTADO, max_length=4, default='ATV')
    

class Topico(models.Model):
    cod_topico = models.AutoField(primary_key=True)
    cod_subforum = models.ForeignKey(Subforum, on_delete=models.CASCADE)
    autor_topico = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=120, default=' ')
    descricao = models.CharField(max_length=512, default=' ')
    data_criacao = models.DateTimeField(default=date.today())
