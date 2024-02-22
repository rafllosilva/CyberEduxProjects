from django.shortcuts import render
from .models import Publicacao, Perfil, Comentario
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def consulta_page(request):
    #publicacoes = Publicacao.objects.filter(estado = "Rio de Janeiro")
    #publicacoes = Publicacao.objects.raw("SELECT * FROM coxinhapp_pessoa WHERE cidade = 'Cuiabá'")
    publicacoes = Publicacao.objects.all()
    return render(request, 'consulta.html', {
        'publicacoes': publicacoes
    })

def home(request):
    publicacoes = Publicacao.objects.all()
    return render(request, 'home.html', {
        'publicacoes': publicacoes,
        'nome': request.user.username,
    })

def cadastro(request):
    if request.method == 'GET':
        return render(request, 'cadastro.html', {
            "email_repeated": False
        })
    elif request.method == 'POST':
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        email = request.POST.get('email')
        if User.objects.filter(username=email).count()>0:
            return render(request, 'cadastro.html', {
            "email_repeated": True
        })
        dt_nascimento = request.POST.get('dt_nascimento')
        descricao = request.POST.get('descricao')
        if "foto" in request.FILES.keys():
            foto = request.FILES['foto']
        else:
            foto = None
        senha = request.POST.get('senha')
        user = User.objects.create_user(email, password=senha)
        user.first_name = nome
        user.last_name = sobrenome
        perfil = Perfil()
        perfil.usuario = user
        perfil.dt_nascimento = dt_nascimento
        perfil.descricao = descricao
        perfil.foto = foto
        perfil.save()
        login(request, user)
        return HttpResponseRedirect('/')
    else:
        return HttpResponseBadRequest()

def detalhes_post(request, id):
    publicacao = Publicacao.objects.get(id=id)
    comentarios = Comentario.objects.filter(publicacao=publicacao)
    if request.method == 'GET':
        return render(request, 'detalhes_post.html', {
            'publicacao': publicacao,
            'comentarios':comentarios,
        })
    elif request.method == 'POST':
        conteudo = request.POST.get("conteudo")
        comentario = Comentario()
        comentario.publicacao = publicacao
        comentario.autor = request.user
        comentario.conteudo = conteudo
        comentario.save()
        return render(request, 'detalhes_post.html', {
            'publicacao': publicacao,
            'comentarios': comentarios,
        })
    else:
        return HttpResponseBadRequest()
        

def login_e_seguranca(request):
    return render(request, 'login_e_seguranca.html', {
        'nome': request.user.username,
    })

def login_view(request):
    if request.method == 'GET':
        return render(request, 'login.html', {
            'incorrect_login': False
        })
    elif request.method == 'POST':
        email = request.POST.get('email')
        password= request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/minha-conta')
        else:
            return render(request, 'login.html', {
                'incorrect_login': True
            })
    else:
        return HttpResponseBadRequest()

@login_required(login_url='/login')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login')

def meus_posts(request):
    return render(request, 'meus_posts.html', {
        'nome': request.user.username,
    })

def meus_comentarios(request):
    return render(request, 'meus_comentarios.html', {
        'nome': request.user.username,
    })

@login_required(login_url='/login')
def minha_conta(request):
    perfil = Perfil.objects.get(usuario=request.user)
    return render(request, 'minha_conta.html', {
        'authenticated': True,
        'perfil': perfil,
        'nome': request.user.username,
        'email': request.user.email,
    })

"""
def minha_conta(request):
    if request.user.is_authenticated:
        # A pessoa está logada!
        pass
        perfil = Perfil.objects.get(usuario=request.user)
        return render(request, 'minha_conta.html', {
            'authenticated': True
        })
    else:
        # A pessoa não está logada!
        return render(request, 'minha_conta.html', {
            'authenticated': False
        })
"""

@login_required(login_url='/login')
def publicar(request):
    if request.method == 'GET':
        return render(request, 'publicar.html', {
        'nome': request.user.username,
    })
    elif request.method == 'POST':
        titulo = request.POST.get('titulo')
        autor = request.POST.get('autor')
        categoria = request.POST.get('categoria')
        conteudo = request.POST.get('conteudo')
        thumbnail = request.FILES['thumbnail']
        publicacao = Publicacao()
        publicacao.titulo = titulo
        publicacao.autor = autor
        publicacao.categoria = categoria
        publicacao.conteudo = conteudo
        publicacao.thumbnail = thumbnail
        publicacao.save()
        return HttpResponseRedirect('/')
    else:
        return HttpResponseBadRequest()

def redes_sociais(request):
    return render(request, 'redes_sociais.html', {
        'nome': request.user.username,
    })

def sobre(request):
    return render(request, 'sobre.html', {
        'nome': request.user.username,
    })