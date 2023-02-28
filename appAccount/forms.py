from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile,ProfilePicture

class CreateuserForm(UserCreationForm):

    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control'
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control'
    }))
    password2 = forms.CharField(label='Confirm_password', widget=forms.PasswordInput(attrs={
        'class':'form-control'
    }))
    class Meta:
        model = User
        fields = ('first_name','last_name','username','password1','password2')


class UserProfileForm(forms.ModelForm):

    # full_name = forms.CharField(widget=forms.TextInput(attrs={
    #     'class':'form-control'
    # }))
    
    class Meta:
        model = Profile
        fields = '__all__'

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = ProfilePicture
        fields= ('image',)