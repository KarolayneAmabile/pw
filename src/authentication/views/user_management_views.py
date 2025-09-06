from authentication.forms.register_form import RegisterForm
from authentication.forms.user_management_forms import AdminUserCreationForm, AdminUserEditForm
from authentication.decorators.group_required import group_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404 
from django.contrib import messages

@group_required(['Mediador'])
def user_management_view(request):
    if request.method == "POST":
        form = AdminUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Novo usuário criado com sucesso!")
            return redirect('user_management')
        else:
            messages.error(request, "Erro ao criar o usuário. Por favor, corrija os campos.")
    else:
        form = AdminUserCreationForm()

    users = User.objects.all().order_by('username')
    
    context = {
        'form': form,
        'users': users
    }
    return render(request, "users/user_management.html", context)

@group_required(['Mediador'])
def user_edit_view(request, user_id):
    user_to_edit = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = AdminUserEditForm(request.POST, instance=user_to_edit)
        if form.is_valid():
            form.save()
            messages.success(request, f"Usuário '{user_to_edit.username}' atualizado com sucesso!")
            return redirect('user_management')
    else:
        form = AdminUserEditForm(instance=user_to_edit)

    return render(request, 'users/user_edit.html', {'form': form, 'user_to_edit': user_to_edit})

@group_required(['Mediador'])
def user_delete_view(request, user_id):
    user_to_delete = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        username = user_to_delete.username
        user_to_delete.delete()
        messages.success(request, f"Usuário '{username}' deletado com sucesso!")
        return redirect('user_management')

    return render(request, 'users/user_delete_confirm.html', {'user_to_delete': user_to_delete})