import requests
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
# Create your views here.


@login_required(login_url='login')
@csrf_exempt
def HomePage(request):
    if request.method == 'POST':
        user_message = request.POST.get('message')
        # Send user message to Rasa and get the bot's response
        rasa_response = send_message_to_rasa(user_message)
        return JsonResponse({'response': rasa_response})
    return render(request, 'home.html')

def send_message_to_rasa(message):
    url = 'http://localhost:5005/webhooks/rest/webhook'  # Example URL, replace with your Rasa server endpoint
    payload = {'message': message}
    response = requests.post(url, json=payload)

    if response.status_code == 200:
        rasa_response = response.json()[0]['text']
        return rasa_response
    else:
        return 'Error communicating with Rasa'


def SignupPage(request):
    if request.method == 'POST':
        user_name = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password1')
        confirm_password = request.POST.get('password2')
        if password != confirm_password:
            return HttpResponse("Your password and confrom password are not Same!!")
        else:
            my_user = User.objects.create_user(user_name, email, password)
            my_user.save()
            return redirect('login')
    return render(request, 'signup.html')


def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('pass')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse("Username or Password is incorrect!!!")
    return render(request, 'login.html')


def LogoutPage(request):
    logout(request)
    return redirect('login')

def ProfilePage(request):
    if request.method == 'POST':
        if 'Save' in request.POST:
            form = User(data=request.POST, instance=request.user)
        if 'Delete' in request.POST:
            del_user(request)
    return render(request, 'profile.html', {"user_name": request.user})

@login_required
def del_user(request):
    user = request.user
    user.delete()
    redirect("login")