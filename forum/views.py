from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import *
#from lais.validacoes import validaData (insira a biblioteca para validar a data )
from validate_docbr import CPF
# Create your views here.


def cadastro(request):
    # Receber os dados
    if request.method == 'POST':
        nome = request.POST.get('nome')
        cpf = request.POST.get('cpf')
        nasc = request.POST.get('nasc')
        grp = request.POST.get('grp')
        teve_covid = request.POST.get('teve_covid')
        senha1 = request.POST.get('senha1')
        senha2 = request.POST.get('senha2')
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
        # if teve_covid == 'sim':
        #    messages.error(request, 'Você teve COVID nos ultimos 30 dias!')
        #    salvar = False
        # if grp == "67" or grp == "65" or grp == "70":
        #    messages.error(
        #        request, 'Seu grupo de atendimento não permite cadastrar!')
        #    salvar = False
        # Se o CPF NÃO estiver cadastrado, então salve os dados user
        if salvar and True:
            try:
                user = User.objects.create_user(
                    username=cpf,
                    password=senha1,)
                user.save()
                cid = cidadao(nome=nome, cpf=user, nasc=nasc,
                              grp_atend=grp, teve_covid=teve_covid, senha=senha1)
                cid.save()
                messages.success(
                    request, 'Cadastro realizado com sucesso!')
            except:
                messages.error(
                    request, 'CPF inválido ou já está cadastrado')
                salvar = False
    # extrair o nome do grupo de atendimento XML


    return render(request, "cadastro.html")

# Historia de Usuario 3 - Página de Login
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