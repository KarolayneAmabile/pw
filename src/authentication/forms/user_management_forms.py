from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.db import transaction

class AdminUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Obrigatório. Um e-mail válido.")
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        label="Cargo",
        required=True,
        help_text="Selecione o cargo do novo usuário."
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este e-mail já está cadastrado.")
        return email

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            # Adiciona o usuário ao grupo selecionado
            group = self.cleaned_data["group"]
            user.groups.add(group)
        return user
    
class AdminUserEditForm(forms.ModelForm):
    """
    Formulário para o admin (Mediador) editar um usuário existente.
    """
    group = forms.ModelChoiceField(queryset=Group.objects.all(), label="Cargo", required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['group'].initial = self.instance.groups.first()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # 'self.instance' é o usuário que está sendo editado
        # Excluímos o próprio usuário da verificação de e-mail
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Este e-mail já está sendo utilizado por outro usuário.")
        return email

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            selected_group = self.cleaned_data['group']
            user.groups.set([selected_group])
        return user