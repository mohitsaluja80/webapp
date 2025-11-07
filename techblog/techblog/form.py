from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from web.models import Comment, Reply, Post


# class createuserForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']


class createuserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
  

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']

        widgets = {
            'content': forms.Textarea(attrs={'rows': 2}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

class NewsletterSubscriptionForm(forms.Form):
    email = forms.EmailField()

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'placeholder': 'Full Name'}))
    subject = forms.CharField(max_length=200,widget=forms.TextInput(attrs={'placeholder': 'Subject'}))
    email = forms.EmailField(max_length=100,widget=forms.TextInput(attrs={'placeholder': 'Your Email'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Type your message..'}))



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        label = { 'content': ""}
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""