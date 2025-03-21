from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import resolve, Resolver404
from .models import *
from djmoney.money import Money

import json

# Create your views here.
@login_required
def index_view(req):
    transactions = Transaction.objects.filter(user=req.user).order_by('-date', '-id')
    accounts = Account.objects.filter(user=req.user)

    context = {
        'transactions': transactions,
        'accounts': accounts,
    }
    return render(req, 'Index.html', context)

def add_transaction(req):
    if req.method == 'POST':
        user = User.objects.get(username=req.user.username)
        data = json.loads(req.body)

        date = data['date']
        value = float(data['value'])
        value = round(value, 2)
        currency = data['currency']
        recipient = data['recipient']
        account = data['account']
        notes = data['notes']

        try:
            account = Account.objects.get(name=account)
        except Account.DoesNotExist:
            try:
                account = Account.objects.get(alias=account)
            except:
                return render(req, 'Index.html', {'error': 'The account does not exist'})
            
        money = None

        try:
            money = Money(value, currency)
        except:
            try:
                money = Money(value, account.valuta)
            except:
                money = Money(value, 'DKK')

        print('date:', date, 'value:', value, 'currency:', currency, 'recipient:', recipient, 'account:', account, 'notes:', notes, 'money:', money)

        Transaction.objects.create(
            user=user,
            date=date,
            value=money,
            recipient=recipient,
            account=account,
            notes=notes,
        )

        return redirect('home_page')
    else:
        return redirect('home_page')

def update_transaction(req):
    if req.method == 'POST':
        data = json.loads(req.body)

        try:
            transaction = Transaction.objects.get(id=data['id'])

            date = data['date']
            value = float(data['value'])
            value = round(value, 2)
            currency = data['currency']
            recipient = data['recipient']
            account = data['account']
            notes = data['notes']
            money = None

            if date != '':
                transaction.date=date
            if value != '':
                try:
                    money = Money(value, currency)
                except:
                    money = Money(value, 'DKK')
                transaction.value=money
            if recipient != '':
                transaction.recipient=recipient
            if account != '':
                try:
                    account = Account.objects.get(name=account)
                    transaction.account = account
                except Account.DoesNotExist:
                    try:
                        account = Account.objects.get(alias=account)
                        transaction.account = account
                    except:
                        return render(req, 'Index.html', {'error': 'The account does not exist'})
            if notes != '':
                transaction.notes=notes
            
            print('id', data['id'], 'date:', date, 'value:', value, 'currency:', currency, 'recipient:', recipient, 'account:', account, 'notes:', notes, 'money:', money)

            transaction.save()
            
        except Transaction.DoesNotExist:
            return render(req, 'Index.html', {'error': 'The transaction does not exist'})

        return redirect('home_page')
    else:
        return redirect('home_page')

def delete_transaction(req):
    if req.method == 'POST':
        data = json.loads(req.body)

        print('delete transaction:', data['id'])
        try:
            transaction = Transaction.objects.get(id=data['id'])
            transaction.delete()
            return redirect('home_page')
        except Exception as e:
            return render(req, 'Index.html', {'error': 'An error occurred while trying to delete the transaction.'})
    else:
        return redirect('home_page')

def add_account(req):
    context= {}
    return render(req, 'Index.html', context)

def update_account(req):
    context= {}
    return render(req, 'Index.html', context)

def delete_account(req):
    if req.method == 'POST':
        data = json.loads(req.body)
        print('delete account:', data['id'])
        try:
            account = Account.objects.get(id=data['id'])
            account.delete()
            return redirect('home_page')
        except Exception as e:
            return render(req, 'Index.html', {'error': 'An error occurred while trying to delete the account.'})
    else:
        return redirect('home_page')

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
        
def delete_user_view(req):
    if req.method == 'POST':
        try:
            user = req.user
            user.delete()
            logout(req)
            return redirect('home_page')
        except Exception as e:
            return render(req, 'Index.html', {'error': 'An error occurred while trying to delete the user.'})
    else:
        return redirect('home_page')

def logout_view(req):
    logout(req)
    return redirect('login')