
import base64
import hashlib

from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
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
    return render(request, 'usuarios/novo_usuario.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                usuario = Usuario.objects.get(email=email, password=hashlib.sha256(password.encode('utf-8')).hexdigest())
                if usuario is not None:
                    request.session['usuario_id'] = usuario.id
                    messages.success(request, 'Login realizado com sucesso!')
                    return redirect('dashboard')
                else:
                    messages.error(request, 'Email ou senha incorretos')
            except Usuario.DoesNotExist:
                messages.error(request, 'Email ou senha incorretos')
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
            arquivo = form.save(commit=False)
            arquivo.usuario_id = request.session.get('usuario_id')

            if 'imagem_base64' in request.FILES:
                arte = request.FILES['imagem_base64']
                img = Image.open(io.BytesIO(arte.read()))
                buffered = io.BytesIO()
                img.save(buffered, format='JPEG')
                arquivo.imagem_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
                img.thumbnail((100, 100))
                buffered = io.BytesIO()
                img.save(buffered, format='JPEG')
                arquivo.thumbnail = base64.b64encode(buffered.getvalue()).decode('utf-8')

            arquivo.save()
            messages.success(request, 'Imagem adicionada com sucesso!')
            return redirect('dashboard')
        else:
            return render(request, 'imagens/adicionar.html', {'form': form})
    else:
        form = ImagemForm()
    return render(request, 'imagens/adicionar_imagem.html', {'form': form})


def galeria(request):
    usuario_id = request.session.get('usuario_id')
    if usuario_id:
        usuario = Usuario.objects.defer('password').get(id=usuario_id)
    else:
        usuario = None
    imagens = Imagem.objects.all()
    context = {
        'usuario': usuario,
        'imagens': imagens,
    }
    print(f'imagens: {imagens}')
    if imagens:
        return render(request, 'imagens/galeria.html', context)

