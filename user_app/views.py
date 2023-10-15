from argparse import RawTextHelpFormatter
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
import bcrypt

from .models import User
    
def home(request):
    user_id = request.session.get('user_id')

    if user_id is not None:
       
        user = User.objects.get(id=user_id)
       
        context = {
            'user' : user,
            'is_authenticated' : True,
        }
    else :
        context = {
            'is_authenticted' : False,
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

        return redirect('home')

def loginPage(request):

    return render(request, 'login.html')

def loginUser(request):
    if request.method == 'POST':
        
        user = User.objects.filter(email=request.POST['email'])

        if user:

            logged_user = user[0]

            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                
                request.session['userid'] = logged_user.id
                
                return redirect('home')

            else:
                error_message = 'Invalid email or password'
                return render(request,'login.html', {'error_message': error_message})
            
        else:
            error_message = 'Invalid email or password'
            return render(request,'login.html', {'error_message': error_message})
            

def logoutUser(request):
    logout(request)
    return redirect('home')
   
    
