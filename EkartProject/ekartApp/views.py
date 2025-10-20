from django.shortcuts import render,redirect
from django.views import View
from django.views.generic import TemplateView
from ekartApp.models import Product,Cart,Order
from ekartApp.forms import UserRegisterForm,UserLoginForm,CartForm,OrderForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.utils.decorators import method_decorator
from ekartApp.authentication import login_required
from django.core.mail import send_mail,settings
from django.utils import timezone
from datetime import timedelta

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
        product_id=kwargs.get("id")
        product=Product.objects.get(id=product_id)
        return render(request,'add_to_cart.html',{"form":form,"product":product})
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
        
class PlaceOrderView(View):
    def get(self,request,*args, **kwargs):
        form=OrderForm()
        cart_id = kwargs.get('id')  # get cart ID from URL
        cart = Cart.objects.get(id=cart_id, user=request.user)
        return render(request,"order.html",{"form":form,"cart":cart})
    
    def post(self,request,*args, **kwargs):
        user=request.user
        email=user.email
        cart_instance=Cart.objects.get(id=kwargs.get('id'))
        address=request.POST.get("address")
        
        # Create the order
        order = Order.objects.create(address=address, user=user, cart=cart_instance)
        
        # Update cart status
        cart_instance.status='order-placed'
        cart_instance.save()
        
        # Send email
        from_addr=settings.EMAIL_HOST_USER
        subject = "Order Confirmation - Ekart"
        message = f"""
        Dear {user.first_name or user.username},

        Thank you for shopping with Ekart! 🎉  
        Order Details:
        Product: {cart_instance.product.product_name}
        Quantity: {cart_instance.quantity}
        Delivery Address: {address}
        """
        send_mail(subject, message, from_addr, [email])
        
        messages.success(request, "Order placed successfully. Confirmation email sent.")
        
        # Redirect using the Order ID
        return redirect("confirmation", id=order.id)


class LogoutView(View):
    def get(self,request):
        logout(request)
        messages.success(request,"Logged Out Succesfully")
        return redirect("login")
    
class OrderConfirmationView(View):
    def get(self, request, *args, **kwargs):
        order_id = kwargs.get('id')
        order = Order.objects.get(id=order_id, user=request.user)

        # Estimate delivery date (3–5 days)
        expected_delivery = timezone.now().date() + timedelta(days=4)

        return render(request, "confirmation.html", {
            "order": order,
            "expected_delivery": expected_delivery
        })
