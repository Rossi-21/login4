from django.urls import path
from . import views

urlpatterns = [

    path('register', views.register, name="register"),
    path('registerUser', views.registerUser, name="registerUser"),
    #path('login', views.loginPage, name="login"),
    path('', views.home, name="home"),
    #path('logout/', views.logoutUser, name="logout"),

]