from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from .MAL_Helper import helper
from django.contrib.auth import authenticate, login, logout
from .models import UserProfile
from django.contrib.auth.models import User
import subprocess
import json

# Create your views here.

def create(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/home/')
    
    if request.method == "POST":
        username = request.POST["username"]
        user = User.objects.filter(username=username)
        if user is not None:
            return render(request, 'MAL_app/create.html', {'error_message': 'Username already exists. Please try again.'})
        password = request.POST["password"]
        email = request.POST["email"]
        
        user = User.objects.create_user(username, email, password)
        UserProfile.objects.create(user=user, refresh_token='', access_token='')
        login(request, user)
        
        return HttpResponseRedirect('/token/')
    return render(request, 'MAL_app/create.html')
   
def home(request):
    return render(request, 'MAL_app/home.html', {'user': request.user})
    
def process_input(request):
    if request.method == 'POST' and 'input_text' in request.POST:
        print(request.POST['input_text'])
        if request.user.is_authenticated:
            token = UserProfile.objects.get(user=request.user).access_token
            output_text = helper.process_message(request.POST['input_text'], token=token)
        else:
            output_text = helper.process_message(request.POST['input_text'])
        return JsonResponse({'output_text': output_text})
    else:
        return JsonResponse({'error': 'Invalid request'})

def login_screen(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/home/')
    error_message = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None
        
        if user is not None:
            authenticated_user = authenticate(request, username=username, password=password)
            if authenticated_user is not None:
                login(request, authenticated_user)
                return HttpResponseRedirect('/home/')
        
        error_message = "Invalid username or password. Please try again."
    
    return render(request, 'MAL_app/login.html', {'error_message': error_message})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login/')

def generate_token_link(request):
    if request.method == 'POST':
        client_id = request.POST.get('clientId')
        code_verifier = subprocess.check_output(['python', 'MAL_app/MAL_Helper/code_verifier.py']).decode('utf-8')
        
        output = subprocess.check_output(['python', 'MAL_app/MAL_Helper/link_generator.py', client_id, code_verifier]).decode('utf-8')
        
        return JsonResponse({'output_link': output, 'code_verification': code_verifier})
    else:
        return JsonResponse({'error': 'Invalid request'})

def token(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')
    user_profile = UserProfile.objects.get(user=request.user)
    if user_profile.access_token != "" or user_profile.refresh_token != "":
        return HttpResponseRedirect('/home/')
    if request.method == "POST":
        code = request.POST["code"]
        client_id = request.POST["clientId"]
        client_secret = request.POST["clientSecret"]
        code_verifier = request.POST["codeVerification"]
        
        output = subprocess.check_output(['python', 'MAL_app/MAL_Helper/token_generator.py', code, code_verifier, client_id, client_secret])
        output = output.decode('utf-8')
        output = output.replace("'", "\"")
        output = json.loads(output)
        print(output)
        
        # check for errors
        if 'error' in output:
            return render(request, 'MAL_app/token.html', {'error_message': output['message'] + ': ' + output['error']})
        
        if 'access_token' in output:
            user_profile.access_token = output['access_token']
            user_profile.refresh_token = output['refresh_token']
            user_profile.save()
            return HttpResponseRedirect('/home/')
        
    return render(request, 'MAL_app/token.html')