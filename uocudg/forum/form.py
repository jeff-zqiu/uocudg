from django import forms
from  django.contrib.auth import forms as auth_form

class PostForm(forms.Form):
    title = forms.CharField(label='Title', max_length=50)
    content = forms.CharField(label='Content', widget=forms.Textarea)

class CommentForm(forms.Form):
    content = forms.CharField(label='Comment', widget=forms.Textarea)

class SignupForm(forms.Form):
    # todo: add email authentication and password confirmation
    username = forms.CharField(label='Username', max_length=30)
    email = forms.EmailField(label='Email', widget=forms.EmailInput)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class AuthenticatinoForm(auth_form.AuthenticationForm):
    pass

