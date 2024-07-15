from django.db import models


# Create your models here.
class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome', 'password']

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        db_table = 'usuarios'
        ordering = ['-criado_em']


class Imagem(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='imagens')
    titulo = models.CharField(max_length=100)
    imagem = models.TextField(unique=True)
    thumbnail = models.TextField(unique=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo

    REQUIRED_FIELDS = ['titulo', 'imagem', 'thumbnail']

    class Meta:
        verbose_name = 'Imagem'
        verbose_name_plural = 'Imagens'
        db_table = 'imagens'
        ordering = ['-criado_em']
