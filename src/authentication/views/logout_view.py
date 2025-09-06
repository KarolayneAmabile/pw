from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "Você saiu da sua conta com sucesso.")
    return redirect("login")