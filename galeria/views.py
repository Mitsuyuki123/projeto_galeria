import base64
import hashlib

from PIL import Image
import io
from django.shortcuts import render, redirect

from galeria.forms import UsuarioForm, ImagemForm, LoginForm

from django.contrib import messages

from galeria.models import Imagem, Usuario


# Create your views here.
def novo_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.password = hashlib.sha256(usuario.password.encode()).hexdigest()
            usuario.save()
            messages.success(request, 'Usuário criado com sucesso!')
            return redirect('login')
        else:
            return render(request, 'usuarios/novo_usuario.html', {'form': form})
    else:
        form = UsuarioForm()
    return render(request, 'usuarios/novo.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            usuario = form.get_usuario()
            request.session['usuario_id'] = usuario.id
            return redirect('dashboard')
        else:
            return render(request, 'usuarios/login.html', {'form': form})
    else:
        form = LoginForm()
    return render(request, 'usuarios/login.html', {'form': form})


def logout(request):
    request.session.flush()
    return redirect('login')


def dashboard(request):
    usuario_id = request.session.get('usuario_id')
    if usuario_id:
        return render(request, 'usuarios/dashboard.html')
    else:
        return redirect('login')


def adicionar_imagem(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')
    if request.method == 'POST':
        form = ImagemForm(request.POST, request.FILES)
        if form.is_valid():
            imagem = form.save(commit=False)
            imagem.usuario_id = request.session.get('usuario_id')
            if 'imagem' in request.FILES:
                imagem = Image.open(request.FILES['imagem'])
                buffer = io.BytesIO()
                imagem.save(buffer, format="JPG")
                imagem.imagem = base64.b64encode(buffer.getvalue()).decode('utf-8')
                imagem = imagem.resize((100, 100), Image.LANCZOS)
                buffer = io.BytesIO()
                imagem.save(buffer, format="JPG")
                imagem.thumbnail = base64.b64encode(buffer.getvalue()).decode('utf-8')
            imagem.save()
            messages.success(request, 'Imagem adicionada com sucesso!')
            return redirect('dashboard')
        else:
            return render(request, 'imagens/adicionar.html', {'form': form})
    else:
        form = ImagemForm()
    return render(request, 'imagens/adicionar.html', {'form': form})


def galeria(request):
    usuario_id = request.session.get('usuario_id')
    if usuario_id:
        usuario = Usuario.objects.defer('password').get(id=usuario_id)
    else:
        usuario = None
    imagens = Imagem.objects.all()
    context = {
        'usuario': usuario,
        'imagens': imagens
    }
    return render(request, 'imagens/galeria.html', {'context': context})
