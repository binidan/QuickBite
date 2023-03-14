from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),
    path('update-user/', views.updateUser, name="update-user"),
    path('update-item/', views.updateItem, name="update-item"),
    path('cart/', views.cartPage, name="cart"),
    path('checkout/', views.checkOutPage, name="checkout"),
    path('address-register', views.addressRegister, name="address-register"),
    path('order/', views.orderPage, name="order"),
]