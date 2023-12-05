from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from ..forms.login_form import CustomLoginForm
from django.shortcuts import redirect

class CustomLoginView(LoginView):
    template_name = "estudiante/estudiante_login.html"
    form_class = CustomLoginForm
    redirect_authenticated_user = True

def logout_view(request):
    logout(request)

    return redirect('list_estudiantes')