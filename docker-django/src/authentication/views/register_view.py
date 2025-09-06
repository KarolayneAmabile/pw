from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.models import Group
from authentication.forms.register_form import RegisterForm

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            try:
                group = Group.objects.get(name='Diretor')
                user.groups.add(group)
            except Group.DoesNotExist:
                messages.error(request, "O grupo 'Diretor' não foi encontrado.")
                user.delete() 
                return redirect('register')

            login(request, user)
            messages.success(request, "Registro bem-sucedido!")
            return redirect("home")
        else:
            messages.error(request, "Falha no registro. Verifique as informações.")
    else:
        form = RegisterForm()
    
    return render(request, "auth/register.html", {"form": form})
