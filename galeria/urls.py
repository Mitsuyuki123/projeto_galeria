from django.urls import path
from . import views

urlpatterns = [
    path('registrar/', views.novo_usuario, name='novo_usuario'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
