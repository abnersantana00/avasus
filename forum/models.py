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
