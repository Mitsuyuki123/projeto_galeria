import hashlib

from django import forms
from .models import Usuario, Imagem


class BootStrapModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label


class UsuarioForm(BootStrapModelForm):
    class Meta:
        model = Usuario
        fields = ['nome', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }


class ImagemForm(BootStrapModelForm):
    class Meta:
        model = Imagem
        fields = ['titulo', 'imagem_base64']

    imagem_base64 = forms.ImageField(required=True, widget=forms.FileInput(attrs={
        'class': 'form-control',
        'accept': 'image/*',
    }))


class LoginForm(forms.Form):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'Digite seu email'
    }))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Digite sua senha'
    }))

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            try:
                user = Usuario.objects.get(email=email)
                hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
                if hashed_password != user.password:
                    raise forms.ValidationError('Senha incorreta')
            except Usuario.DoesNotExist:
                raise forms.ValidationError('Email não encontrado')

        return cleaned_data
