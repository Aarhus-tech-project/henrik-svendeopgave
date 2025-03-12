from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import resolve, Resolver404
from .models import *

import json

# Create your views here.
@login_required
def index_view(req):
    context = {}
    return render(req, 'Index.html', context)

def login_view(req):
    if req.method == 'POST':
        data = json.loads(req.body)

        password = data['password']
        usernameOrEmail = data['username_or_email']
        nextUrl = data['next_url']
        print(usernameOrEmail)
        if '@' in usernameOrEmail:
            username = User.objects.get(email=usernameOrEmail).username
        else:
            username = usernameOrEmail
        
        user = authenticate(req, username=username, password=password)
        
        if user is not None:
            login(req, user)
            try:
                resolve(nextUrl)
                return redirect(nextUrl)
            except Resolver404:
                return redirect('home_page')
        else:
            if User.objects.filter(username=username): 
                return render(req, 'Login.html', {'error': 'Incorrect password'})
            else:
                return render(req, 'Login.html', {'error': 'User does not exist'})
    else:
        return render(req, 'Login.html')

def signup_view(req):
    if req.method == 'POST':
        data = json.loads(req.body)

        username = data['username']
        email = data['email']
        password = data['password']
        confirm_password = data['confirm_password']
        nextUrl = data['next_url']
        
        try:
            User.objects.get(username=username)
            return render(req, 'Signup.html', {'error': 'User already exists'})
        except User.DoesNotExist:
            try:
                User.objects.get(email=email)
                return render(req, 'Signup.html', {'error': 'User already exists'})
            except User.DoesNotExist:
                    if password == confirm_password:
                        user = User.objects.create_user(username=username, email=email, password=password)
                        user.save()
                        print(user)
                        authenticateUser = authenticate(req, username=username, password=password)
                        if authenticateUser is not None:
                            login(req, authenticateUser)
                            try:
                                resolve(nextUrl)
                                return redirect(nextUrl)
                            except Resolver404:
                                return redirect('home_page')
                        else:
                            return render(req, 'Login.html', {'error': 'Error during login'})
                    else:
                        return render(req, 'Signup.html', {'error': 'Passwords do not match'})
    else:
        context = {}
        return render(req, 'Signup.html', context)
    
def update_user_view(req):
    if req.method == 'POST':
        try:
            user = User.objects.get(username=req.user.username)
            username = req.POST['username']
            email = req.POST['email']
            first_name = req.POST['first_name']
            last_name = req.POST['last_name']
            password = req.POST['password']
            confirm_password = req.POST['confirm_password']

            print(username, email, first_name, last_name, password, confirm_password)
            
            if username == user.username:
                username = ''
            if email == user.email:
                email = ''
            if first_name == user.first_name:
                first_name = ''
            if last_name == user.last_name:
                last_name = ''

            if username != '' and user.username != username:
                try:
                    User.objects.get(username=username)
                    return render(req, 'Index.html', {'error': 'Username already exists', 'type': 'user'})
                except User.DoesNotExist:
                    user.username = username
            if email != '':
                try:
                    User.objects.get(email=email)
                    return render(req, 'Index.html', {'error': 'Email already exists', 'type': 'user'})
                except User.DoesNotExist:
                    user.email = email
            if first_name != '':
                user.first_name = first_name
            if last_name != '':
                user.last_name = last_name
            if password == confirm_password and password != '':
                user.set_password(password)
            
            user.save()
            return redirect('home_page')
        except User.DoesNotExist:
            return render(req, 'Login.html', {'error': 'User does not exist'})
        
def delete_account_view(req):
    if req.method == 'POST':
        try:
            user = req.user
            user.delete()
            logout(req)
            return redirect('home_page')
        except Exception as e:
            return render(req, 'Index.html', {'error': 'An error occurred while trying to delete the account.'})
    else:
        return redirect('home_page')

def logout_view(req):
    logout(req)
    return redirect('login')