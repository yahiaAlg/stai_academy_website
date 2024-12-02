from django import forms
from .models import Notice, Profile
from django.contrib.auth.models import User, Group


class LoginForm(forms.Form):
    username = forms.CharField(
        label="اسم المستخدم",
        widget=forms.TextInput(attrs={"placeholder": "أدخل اسم المستخدم الخاص بك"}),
    )
    password = forms.CharField(label="Password", widget=forms.PasswordInput())


class RegisterForm(forms.Form):
    username = forms.CharField(
        label="اسم المستخدم",
        max_length=150,
        widget=forms.TextInput(attrs={"placeholder": "أدخل اسم المستخدم الخاص بك"}),
    )
    email = forms.EmailField(
        label="البريد الإلكتروني",
        required=False,
        widget=forms.EmailInput(attrs={"placeholder": "إدخال بريدك الإلكتروني"}),
    )
    phone = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "أدخل رقم هاتفك"}),
    )
    password = forms.CharField(label="كلمة مرور", widget=forms.PasswordInput())
    confirm_password = forms.CharField(
        label="تأكيد كلمة المرور", widget=forms.PasswordInput()
    )
    group = forms.ChoiceField(
        label="نوع  المستخدم",
        choices=[("", "---الرجاء تحديد خيار---")]
        + list(Group.objects.all().values_list("id", "name")),
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("كلمات المرور لا تتطابق")
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("اسم المستخدم موجود بالفعل")
        return username


class AddNoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = "__all__"
