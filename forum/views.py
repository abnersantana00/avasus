from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import CustomUser
from .manager import *
from django.contrib.auth import *
#from avasus.validacoes import validaData (insira a biblioteca para validar a data )
from validate_docbr import CPF
from forum.validacoes import validaData
from django.contrib.auth import login as authlogin, logout
import datetime


from time import time
import calendar
# Create your views here.

def cadastro(request):
    # Receber os dados
    if request.method == 'POST':
        nome_completo = request.POST.get('nome_completo')
        nome_social = request.POST.get('nome_social')
        cpf = request.POST.get('cpf')
        nasc = request.POST.get('nasc')
        estado = request.POST.get('estado')
        cidade = request.POST.get('cidade')
        senha1 = request.POST.get('senha1')
        senha2 = request.POST.get('senha2')
        termos = request.POST.get('termos')
        print(nome_completo, nome_social, cpf, nasc, estado, cidade, senha1, senha2, termos)
    # validar CPF
        salvar = True
        _cpf = CPF()
        if _cpf.validate(cpf) == False:
            messages.error(request, 'CPF Inválido!')
            salvar = False
    # Validar a Data Nascimento
        if validaData(nasc) == False:
            messages.error(request, 'Data inválida ou Menor de 18 anos!')
            salvar = False
    # Validar a senha
        if senha1 != senha2:
            messages.error(request, 'As senhas não conferem!')
            salvar = False
    # validar termos de uso
        if termos != 'sim':
            messages.error(request, 'Voce precisa concordar com os temos de uso!')
            salvar = False
        if salvar and True:
            try:
                CustomUser.objects.create(nome_completo=nome_completo, nome_social=nome_social, cpf=cpf, nasc=nasc, estado=estado, cidade=cidade)
                messages.success(
                    request, 'Cadastro realizado com sucesso!')
            except:
                messages.error(
                    request, 'Usuario já está cadastrado')
                salvar = False
    return render(request, "cadastro.html")


def login(request):
    if request.user.is_authenticated == True:
        return redirect('pag-inicial')
    if request.method == 'POST':
        cpf = request.POST.get('cpf')
        senha = request.POST.get('senha')
        # verrificar se CPF e Senha informada é igual no BD
        user = authenticate(request, cpf=cpf, password=senha)
        print("  USERRR  ", user)
        if user is not None:
            authlogin(request,user)
            return redirect('pag-inicial')
        else:
            messages.error(request, 'CPF ou Senha Incorreta!')
    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect('/')

def pag_inicial(request):
    # se usuario esta autenticado libere
    if request.user.is_authenticated == True:

        cpf = request.user.cpf
        nome = request.user.nome_completo
        nasc = CustomUser.objects.filter(cpf=cpf).values_list('nasc')
        dias_ano = 365.2425
        idade = int((datetime.date.today() - nasc[0][0]).days / dias_ano)
       
    
       

        context = {
            'cpf' : str(cpf),
            'nome' : str(nome),
            'idade' : str(idade),
            'nasc' : nasc[0][0],
        }
        return render(request, "pag-inicial.html", context)
    else:
        return redirect('/') # se nao autenticado redireciona pra login
    
    
    