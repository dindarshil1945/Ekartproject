from django.contrib.auth.models import User
from django import forms
from ekartApp.models import Cart,Order

class UserRegisterForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','email','password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
            'password': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}),  # visible password
        }

class UserLoginForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}),
            'password': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}),  # visible password
        }

class CartForm(forms.ModelForm):
    class Meta:
        model=Cart
        fields=['quantity']
        widgets={
            'qauntity':forms.NumberInput(attrs={'class':'form-control'})
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model=Order
        fields=['address']
        widgets={
            'address':forms.Textarea(attrs={"class":"form-control"})
        }