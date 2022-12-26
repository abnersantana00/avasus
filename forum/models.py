from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class cidadao(models.Model):
    nome_completo = models.CharField(max_length=50)
    nome_social = models.CharField(max_length=50)
    cpf = models.ForeignKey(
        User, on_delete=models.CASCADE, default=None, primary_key=True, related_name='fk')
    nasc = models.DateField(
        "nasc", auto_now=False, auto_now_add=False)
    estado = models.CharField("estado", max_length=2)
    senha = models.CharField("senha", max_length=12)
    TIPO_CIDADAO = (
        ("PROF", "Professor"),
        ("ALU", "Aluno"),
    )
    perfil = models.CharField(choices=TIPO_CIDADAO, max_length=10)

    def __str__(self):
        return self.nome