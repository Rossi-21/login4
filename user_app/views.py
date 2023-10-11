from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
import bcrypt

from .models import User
    
def home(request):
    print(request.user.is_authenticated)    
    return render(request, "index.html")
        

def register(request):
    return render(request, 'register.html')

def registerUser(request):
    errors = User.objects.Validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request,value)

            return redirect('register')
        
    else:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        user = User.objects.create(
                first_name = first_name, last_name = last_name, email = email, password = pw_hash
        )
        print(user.id, user.first_name, user.last_name, user.email, user.password)

        login(request, user)

        return redirect('home')
