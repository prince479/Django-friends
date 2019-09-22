from django import forms
from .models import  Signup,Profile
class LoginForm(forms.Form):
    email=forms.EmailField(widget=forms.TextInput())
    password=forms.CharField(max_length=100,widget=forms.PasswordInput())

class SignupForm(forms.ModelForm):
    class Meta:
        model=Signup
        widgets = {
            'password': forms.PasswordInput(),
        }
        fields='__all__'


class ViewProfile(forms.ModelForm):
    class Meta:
        model=Profile
        fields='__all__'
class EditProfile(forms.ModelForm):
    class Meta:
        model=Profile
        exclude=['user','paddr','company','friends']

