from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.conf import settings
import bcrypt, requests

from .models import User

api_key = settings.API_KEY

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

def api(request):
    user_id = request.session.get('user_id')
    
    if user_id is not None:
        
        user = User.objects.get(id=user_id)

        url = "https://deezerdevs-deezer.p.rapidapi.com/search" 

        search = request.GET.get('search')
        querystring = {"q" : search}

        headers = {
            "X-RapidAPI-Key": api_key ,
            "X-RapidAPI-Host": "deezerdevs-deezer.p.rapidapi.com"
            }   

        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()

        context = {
            'user' : user,
            'is_authenticated' : True,
            'data': data,
        }

    else:
        context = {
            'is_authenticated' : False
        }

    return render(request, "api.html", context)
        
def registerPage(request):
    return render(request, 'register.html')

def registerUser(request):
    # if the method from the registration form is a POST method
    if request.method == 'POST':

        # call errors from the Validator
        errors = User.objects.Validator(request.POST)
        # if there are errors
        if len(errors) > 0:
            # loop through the errors
            for key, value in errors.items():
                # display the errors as a message
                messages.error(request, value)
            
            return redirect('register')
            
        else:
            # grab the input of the form
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            password = request.POST['password']
            # hash the password
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            # create a user boject with the information the user enter in the form
            user = User.objects.create(
                    first_name = first_name, last_name = last_name, email = email, password = pw_hash
            )
            # set the user id in session
            request.session['user_id'] = user.id 

            return redirect('home')

def loginPage(request):

    return render(request, 'login.html')

def loginUser(request):
    if request.method == 'POST':
        # pull the email/username from the datatbase
        user = User.objects.filter(email=request.POST['email'])

        if user:
            # if there is a match, create a variable with the fist item of the list pulled from the database
            logged_user = user[0]
            # check the password against the password stored in the database for the logged_user
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                # place their user id into session
                request.session['user_id'] = logged_user.id
                
                return redirect('home')

            else:
                # if the password does not match display an error message
                error_message = 'Invalid email or password'
                return render(request,'login.html', {'error_message': error_message})
            
        else:
            # if the user is not found in the database display an error message
            error_message = 'Invalid email or password'
            return render(request,'login.html', {'error_message': error_message})
            

def logoutUser(request):
    logout(request)
    return redirect('home')
   
    
