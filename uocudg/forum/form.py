from django import forms

class PostForm(forms.Form):
    title = forms.CharField(label='Title', max_length=50)
    content = forms.CharField(label='Content', widget=forms.Textarea)

class CommentForm(forms.Form):
    content = forms.CharField(label='Comment', widget=forms.Textarea)

