from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import CustomUser, Subforum, Categoria, Topico
from .manager import *
from django.contrib.auth import *
#from avasus.validacoes import validaData (insira a biblioteca para validar a data )
from validate_docbr import CPF
from forum.validacoes import validaData
from django.contrib.auth import login as authlogin, logout
import datetime
from django.utils import timezone
from .manager import *
from django.db.models import Count

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
                CustomUser.objects.create_user(nome_completo=nome_completo, nome_social=nome_social, cpf=cpf, nasc=nasc, estado=estado, cidade=cidade, password=senha1)
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
        perfil =  CustomUser.objects.filter(cpf=cpf).values_list('perfil')
        if  perfil[0][0] == 'ALU':
            bloquear = 'disabled'
        else:
            bloquear=''
        # cadastrar novo subforum (Se for professor)
        _cpf = CustomUser.objects.filter(cpf=cpf)
        if request.method == 'POST' and perfil != 'ALU':
            titulo = request.POST.get('titulo')
            desc = request.POST.get('desc')
            categoria = request.POST.get('categoria')
        # salvar no banco o subforum criado pelo professor
            cat_select = Categoria.objects.filter(id=categoria[0])
            
            
            try:
                Subforum.objects.get_or_create(autor = _cpf[0], cat_subforum =cat_select[0]  ,titulo=titulo, descricao=desc, data_criacao=datetime.date.today(), estado='Ativado' )
                messages.success(
                    request, 'Cadastro realizado com sucesso!')
            except:
               
                messages.error(
                    request, 'Algo deu errado')
       
        
        
      
        subforuns_assoc = len(Subforum.objects.filter(autor=_cpf[0]))

        subforums = list(Subforum.objects.filter(autor_id=_cpf[0]).values_list('titulo','descricao', 'autor','cod_subforum'))
        ### contar os topicos
        topicos = list((Topico.objects.values('cod_subforum').annotate(dcount=Count('cod_subforum'))))
        #print(listagem_subforums)
        #print(topicos)

        #x = listagem_subforums.intersection(topicos)
        #print(x)
        listagem_subforums = []
        for titulo, descricao, autor, cod_subforum in subforums:
            #print(cod_subforum)
            for n in topicos:
                if cod_subforum == n['cod_subforum']:
                    #print("eh igual: ",cod_subforum, '=', n['cod_subforum'])
                    listagem_subforums.append((titulo, descricao,autor,cod_subforum,n['dcount']))
            if listagem_subforums[-1][3] != cod_subforum:
                listagem_subforums.append((titulo, descricao,autor,cod_subforum,0))
            
            
            
                


            # se ja ta listado não liste, se não então pode listar É AQUI QUE TEM QUE MUDAR O BAGULHO
            #listagem_subforums.append((titulo, descricao,autor,cod_subforum,0))
            #listagem_subforums.append((titulo, descricao,autor,cod_subforum,0))    
            #print(cod_subforum, '=', n1['cod_subforum'])
    
        
           

      
       
        

        context = {
            'cpf' : str(cpf),
            'nome' : str(nome),
            'idade' : str(idade),
            'nasc' : nasc[0][0],
            'bloquear' : bloquear,
            'subforuns_assoc' : subforuns_assoc,
            'listagem_subforums' : listagem_subforums
            
        }
        return render(request, "pag-inicial.html", context)
    else:
        return redirect('/') # se nao autenticado redireciona pra login
    
    
def post_subforum(request, cod_subforum):
    if request.user.is_authenticated == True:
        context = {
        'cod_subforum': 1
        }
        return render(request, "subforum.html", context)