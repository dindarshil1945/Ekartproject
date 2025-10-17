from django.shortcuts import render,redirect
from django.views import View
from django.views.generic import TemplateView
from ekartApp.models import Product,Cart
from ekartApp.forms import UserRegisterForm,UserLoginForm,CartForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.utils.decorators import method_decorator
from ekartApp.authentication import login_required

# Create your views here.

class HomeView(View):
    def get(self,request):
        products=Product.objects.all()
        return render(request,"index.html",{"products":products})

class DetailView(View):
    def get(self,request,**kwargs):
        product_id=kwargs.get("id")
        product=Product.objects.get(id=product_id)
        return render(request,"detail_view.html",{"product":product})
    
class UserRegisterView(View):
    def get(self,request):
        form=UserRegisterForm()
        return render(request,"register.html",{"form":form})
    def post(self,request):
        form=UserRegisterForm(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            messages.success(request,"User Registered Succesfully")
            return redirect("login")
        else:
            messages.warning(request,"Invalid Input")
            return redirect("register")

class UserLoginView(View):
    def get(self,request):
        form=UserLoginForm()
        return render(request,"login.html",{"form":form})
    
    def post(self,request):
        username=request.POST.get('username')
        password=request.POST.get('password')
        res=authenticate(request,username=username,password=password)
        if res:
            login(request,res)
            messages.success(request,"Login Succesful")
            return redirect("home_view")
        else:
            messages.warning(request,"Invalid credentials")
            return HttpResponse("Invalid credentials")

@method_decorator(login_required,name='dispatch')
class AddToCartView(View):
    def get(self,request,*args, **kwargs):
        form=CartForm()
        return render(request,'add_to_cart.html',{"form":form})
    def post(self,request,*args, **kwargs):
        product=Product.objects.get(id=kwargs.get("id"))
        user=request.user
        quantity=request.POST.get('quantity')
        cart_items=Cart.objects.filter(user=user,product=product,status='in-cart')
        if cart_items:
            cart_items[0].quantity+=int(quantity)
            cart_items[0].save()
            messages.success(request,"item added to cart")
            return redirect("home_view")
        else:
            Cart.objects.create(user=user,product=product,quantity=quantity)
            return redirect('home_view')

class CartListView(View):
    def get(self,request):
        if not request.user.is_authenticated:
            return redirect('login')
        else:
            cart_list=Cart.objects.filter(user=request.user,status='in-cart')
            return render(request,'cart_view.html',{"cartlist":cart_list})

class LogoutView(View):
    def get(self,request):
        logout(request)
        messages.success(request,"Logged Out Succesfully")
        return redirect("login")
    