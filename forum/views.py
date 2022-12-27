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
    # validar os dados recebidos
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
                user = CustomUser.objects.create(nome_completo=nome_completo, nome_social=nome_social, cpf=cpf, nasc=nasc, estado=estado, cidade=cidade)
                print('printando USER', user)
                #user = User.objects.create_user(
                #    username=cpf,
                #    password=senha1,)
                #user.save()
                #cid = cidadao(nome=nome, cpf=user, nasc=nasc,
                #              grp_atend=grp, teve_covid=teve_covid, senha=senha1)
                #cid.save()
                messages.success(
                    request, 'Cadastro realizado com sucesso!')
            except:
                messages.error(
                    request, 'CPF inválido ou já está cadastrado')
                salvar = False
    # extrair o nome do grupo de atendimento XML
   
    grp_atend = {}
    i = 1


    return render(request, "cadastro.html", {"grp_atend": grp_atend})


def login(request):
    if request.method == 'POST':
        cpf = request.POST.get('cpf')
        senha = request.POST.get('senha')
        # verrificar se CPF e Senha informada é igual no BD
        user = authenticate(request, username=cpf, password=senha)
        if user is not None:
            login(request, user)
            return redirect('pag-inicial')
        else:
            messages.error(request, 'CPF ou Senha Incorreta!')
    return render(request, "login.html")