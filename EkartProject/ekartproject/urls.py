"""
URL configuration for ekartproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ekartApp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register', views.UserRegisterView.as_view(),name="register"),
    path('', views.UserLoginView.as_view(),name="login"),
    path('home', views.HomeView.as_view(),name="home_view"),
    path('detailView/<int:id>', views.DetailView.as_view(),name="detail_view"),
    path('add/cart/<int:id>', views.AddToCartView.as_view(),name="add_to_cart"),
    path('cart', views.CartListView.as_view(),name="cart_view"),
    path('order/<int:id>', views.PlaceOrderView.as_view(),name="cart_order_view"),
    path('order/confirmation/<int:id>/', views.OrderConfirmationView.as_view(), name='confirmation'),
    path('logout', views.LogoutView.as_view(),name="logout"),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
