from django import forms
from captcha.fields import CaptchaField

class BottleUserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128)
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput)
    verification = CaptchaField()

class RegisterForm(forms.Form):
    gender = (
        ('1', "男"),
        ('0', "女"),
    )
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    name = forms.CharField(label="昵称", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    sex = forms.ChoiceField(label='性别', choices=gender)
    email = forms.EmailField(label='邮箱',error_messages={'required': '邮箱不能为空', 'invalid': '邮箱格式错误'})
    description = forms.CharField(label='简介',max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    verification = CaptchaField()

class ForgetForm(forms.Form):
    email = forms.EmailField(label='邮箱',error_messages={'required': '邮箱不能为空', 'invalid': '邮箱格式错误'})
    verification = CaptchaField()