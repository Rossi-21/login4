from argparse import RawTextHelpFormatter
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
import bcrypt

from .models import User
    
def home(request):

    user_id = request.session.get('user_id')
    first_name = request.session.get('first_name')

    context = {
        'user_id' : user_id,
        'first_name' : first_name
    }

    return render(request, "index.html", context)
        
def registerPage(request):
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
        
        request.session['user_id'] = user.id
        request.session['first_name'] = user.first_name 

        print(user.id, user.first_name, user.last_name, user.email, user.password)

        return redirect('home')

def loginPage(request):

    return render(request, 'login.html')

def loginUser(request):
    if request.method == 'POST':
        
        user = User.objects.get(email = request.POST['email'])

        if user:

            if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
                
                request.session['userid'] = user.id
                
                return redirect('home')

            else:
                return redirect('login')


   
    
