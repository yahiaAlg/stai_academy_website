from django import forms
from .models import Notice
from django.contrib.auth.models import User,Group
from django.contrib.auth.forms import UserCreationForm

class LoginUserForm(UserCreationForm):
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={'placeholder':'Enter your username'}))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    def __init__(self, *args, **kwargs):
        super(LoginUserForm, self).__init__(*args, **kwargs)
        del self.fields['password2']
    class Meta:
        model = User
        fields = ["username",  "password1"]
        labels = {
            'username': ('Username'),
            'password1': ("Password")
        }
class RegisterUserForm(UserCreationForm):
    group = forms.ChoiceField(
        choices=[("", "---Please select an option---")]
        + list(
            Group.objects.all().values_list(
                "id","name"
            )
        )
    )
    
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "group"]


class AddNoticeForm(forms.ModelForm):
    class Meta:
        model=Notice
        fields="__all__"
