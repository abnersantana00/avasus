from django.shortcuts import render
# Create your views here.
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import CustomUser, Subforum, Categoria, Topico, Resposta, VinculoSubforum
from .manager import *
from django.contrib.auth import *
#from avasus.validacoes import validaData (insira a biblioteca para validar a data )
from validate_docbr import CPF
from forum.validacoes import validaData
from django.contrib.auth import login as authlogin, logout
import datetime
from django.utils import timezone
from .manager import *
from django.db.models import Count, Max, Min, Sum
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
           
            obj = Subforum(autor = _cpf[0], nome_autor=str(nome), nome_social = request.user.nome_social, cat_subforum =cat_select[0]  ,titulo=titulo, descricao=desc, data_criacao=datetime.date.today(), estado='Ativado' )
            obj.save()
            id_subforum = Subforum.objects.filter(cod_subforum=obj.cod_subforum) 
            usuario_vinculado = CustomUser.objects.filter(cpf=request.user.cpf)
           
            # criar um vinculo na tabela de vinculos
            print(id_subforum, type(id_subforum))
            print(usuario_vinculado, type(usuario_vinculado))
            VinculoSubforum.objects.get_or_create(cod_subforum=id_subforum[0], aluno= usuario_vinculado[0]) 
            
            try:
                #obj = Subforum(autor = _cpf[0], nome_autor=str(nome), nome_social = request.user.nome_social, cat_subforum =cat_select[0]  ,titulo=titulo, descricao=desc, data_criacao=datetime.date.today(), estado='Ativado' )
                #obj.save()
                #id_subforum = obj.cod_subforum
                # criar um vinculo na tabela de vinculos
                #usuario_vinculado = CustomUser.objects.filter(cpf=request.user.cpf)
                #VinculoSubforum.objects.get_or_create(cod_subforum=id_subforum, aluno= usuario_vinculado[0]) 
                #messages.success(
                #    request, 'Cadastro realizado com sucesso!')
                ...
            except:
                ...
               
             
       
        subforuns_assoc = len(VinculoSubforum.objects.filter(aluno=_cpf[0]))
        vinculo_subforum =VinculoSubforum.objects.values_list('aluno', 'cod_subforum').filter(aluno=_cpf[0])
        subforums = list(Subforum.objects.values_list('titulo','descricao', 'nome_autor','cod_subforum', 'autor_id') )




        topicos = list((Topico.objects.values('cod_subforum').annotate(dcount=Count('cod_subforum'))))
        listagem_subforums = []
        for titulo, descricao, autor, cod_subforum, autor_id in subforums:
            
            for cod_vinc in vinculo_subforum:
                if cod_subforum == cod_vinc[1] or str(autor_id) == str(request.user.cpf):
                    for n in topicos:
                        
                        if cod_subforum == n['cod_subforum']:
                            listagem_subforums.append((titulo, descricao,autor,cod_subforum,n['dcount']))
                    
                    try:
                        if listagem_subforums[-1][3] != cod_subforum:
                            listagem_subforums.append((titulo, descricao,autor,cod_subforum,0))
                    except:
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
        usuarios = CustomUser.objects.values_list('cpf','nome_social')
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
            cod_topico = request.POST.get('cod_topico')
            trancar_topico = request.POST.get('trancar_topico')
            texto_resposta = request.POST.get('texto_resposta')
            _nome = request.user.nome_social
            cpf_vinculo = request.POST.get('cpf_vinculo')

            

            if len(_nome) < 2:
                _nome = request.user.nome_completo

            
            try:
                Topico.objects.create(cod_subforum =_cod_subforum[0], autor= _autor[0], nome_autor=_nome, titulo=titulo, descricao=descricao, data_criacao=datetime.datetime.now(), estado='Ativado' )
                messages.success( request, 'Topico criado com sucesso!')
            except:
                messages.error(
                        request, 'Algo deu errado')
             # Receber resposta
            _cod_topico = Topico.objects.filter(cod_topico=cod_topico)
            try:
                if _cod_topico.values_list('estado')[0][0] == 'Ativado':
                    Resposta.objects.get_or_create(cod_topico =_cod_topico[0], autor= _autor[0], nome_autor=_nome, texto=texto_resposta, data_criacao=datetime.datetime.now())
                    messages.success(
                            request, 'Topico criado com sucesso!')
            except:
                ...
            # Trancar tópico
            perfil =  CustomUser.objects.filter(cpf=request.user.cpf).values_list('perfil')
            
            if trancar_topico == 'sim'and perfil[0][0] == 'PROF':
                try:
                    _cod_topico.update(estado="TRC")
                except:
                    ...

            aluno_vinculado = CustomUser.objects.filter(cpf=cpf_vinculo)
            if perfil[0][0] == 'PROF':
                try:
                    VinculoSubforum.objects.get_or_create(cod_subforum=_cod_subforum[0], aluno= aluno_vinculado[0]) 
                except:
                    ...
            return redirect('/'+str(cod_subforum))

        perfil =  CustomUser.objects.filter(cpf=request.user.cpf).values_list('perfil') 
        respostas = Resposta.objects.values_list('cod_topico', 'autor', 'nome_autor', 'texto', 'data_criacao').order_by('-data_criacao')
        qtd_respostas = Resposta.objects.values_list('cod_topico').annotate(dcount=Count('cod_topico'))
        ultima_postagem = Resposta.objects.values_list('cod_topico').annotate(dcount=Max('data_criacao'))
        alunos_vinculados = VinculoSubforum.objects.values_list('aluno', 'cod_subforum').annotate(dcount=Count('cod_subforum')).order_by('cod_subforum')
        alunos_vinc_subforum = 0
        if len(alunos_vinculados)>0:
            for i in range(len(alunos_vinculados)):
                if cod_subforum == str(alunos_vinculados[i][1]):
                    alunos_vinc_subforum = alunos_vinc_subforum+1
        
           
        
        context = {
            'cod_subforum': cod_subforum,
            'alunos_vinc_subforum' : alunos_vinc_subforum,
            'topicos' : topicos,
            'categoria': categoria[0][0],
            'total_postagens' : total_postagens,
            'respostas' : respostas,
            'qtd_respostas' : qtd_respostas,
            'ultima_postagem' : ultima_postagem,
            'usuarios' : usuarios,
            'perfil' : perfil[0][0]
            }
        return render(request, "subforum.html", context)
        