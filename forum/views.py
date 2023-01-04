from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import CustomUser, Subforum, Categoria, Topico, Resposta
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

        subforums = list(Subforum.objects.filter(autor_id=_cpf[0]).values_list('titulo','descricao', 'nome_autor','cod_subforum', 'nome_autor'))
        ### contar os topicos
        topicos = list((Topico.objects.values('cod_subforum').annotate(dcount=Count('cod_subforum'))))
   
        listagem_subforums = []
        for titulo, descricao, autor, cod_subforum, nome_autor in subforums:
   
            for n in topicos:
                if cod_subforum == n['cod_subforum']:
                    listagem_subforums.append((titulo, descricao,autor,cod_subforum,n['dcount']))
            if listagem_subforums[-1][3] != cod_subforum:
                listagem_subforums.append((titulo, descricao,autor,cod_subforum,0))
            
            
            
                


    
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
        topicos = Topico.objects.filter(cod_subforum=cod_subforum).values_list('cod_topico', 'nome_autor', 'titulo', 'descricao', 'data_criacao', 'estado').order_by('-data_criacao')
        cod_categoria = Subforum.objects.filter(cod_subforum=cod_subforum).values_list('cat_subforum')
        categoria = Categoria.objects.filter(id=cod_categoria[0][0]).values_list('nome')
        total_postagens = len(topicos)
        # criar novo topico
        if request.method == 'POST':
            titulo = request.POST.get('titulo_topico')
            descricao = request.POST.get('descricao_topico')

            _cod_subforum = Subforum.objects.filter(cod_subforum=cod_subforum)
            _cpf = CustomUser.objects.filter(cpf=request.user.cpf)
            _autor = CustomUser.objects.filter(cpf=request.user.cpf)

            _nome = request.user.nome_social
            if len(_nome) < 2:
                _nome = request.user.nome_completo

            

            try:
                Topico.objects.get_or_create(cod_subforum =_cod_subforum[0], titulo=titulo, autor= _autor[0], nome_autor=_nome, descricao=descricao, data_criacao=datetime.datetime.now(), estado='Ativado' )
                messages.success( request, 'Topico criado com sucesso!')
            except:
                messages.error(
                        request, 'Algo deu errado')
            
             # Receber resposta
        
            cod_topico = request.POST.get('cod_topico')
            texto_resposta = request.POST.get('texto_resposta')
        
            _cod_topico = Topico.objects.filter(cod_topico=cod_topico)

            
            try:
                Resposta.objects.get_or_create(cod_topico =_cod_topico[0], autor= _autor[0], nome_autor=_nome, texto=texto_resposta, data_criacao=datetime.datetime.now())
                messages.success(
                        request, 'Topico criado com sucesso!')
            except:
                messages.error(
                        request, 'Algo deu errado')

            return redirect('/'+str(cod_subforum))

       

         
            
        
        
        total_respostas = Resposta.objects.values_list('cod_topico', 'autor', 'nome_autor', 'texto', 'data_criacao').order_by('-data_criacao')
        for i in total_respostas:
            print(i)

        context = {
            'cod_subforum': cod_subforum,
            'topicos' : topicos,
            'categoria': categoria[0][0],
            'total_postagens' : total_postagens,
            'total_respostas' : total_respostas,
            }

        return render(request, "subforum.html", context)
        