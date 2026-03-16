from django.urls import path
from core.views import generar_documentos_view
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect

def home(request):
    if request.user.is_authenticated:
        return redirect('generar_documentos')
    return redirect('login')

urlpatterns = [
    path('', home, name='home'),
    path(
    "login/",
    auth_views.LoginView.as_view(
        template_name="registration/login.html",
        redirect_authenticated_user=True
    ),
    name="login"
    ),
    path("generar-documentos/", generar_documentos_view, name="generar_documentos"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]