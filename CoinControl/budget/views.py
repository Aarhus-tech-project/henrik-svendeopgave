from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import resolve, Resolver404
from .models import *
from djmoney.money import Money
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import json

# Create your views here.
@login_required
def index_view(req):
    transactions = Transaction.objects.filter(user=req.user).order_by('-date', '-id')
    p = Paginator(transactions, 50)
    pageNumber = req.GET.get('page')

    try:
        page_obj = p.page(pageNumber)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)


    accounts = Account.objects.filter(user=req.user)

    context = {
        'transactions': page_obj,
        'p': p,
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
        accountId = data['id']
        notes = data['notes']

        try:
            account = Account.objects.get(id=accountId)
            print('name')
        except Account.DoesNotExist:
            return render(req, 'Index.html', {'error': 'The account does not exist'})
            
        money = None

        try:
            money = Money(value, currency)
        except:
            money = Money(value, 'DKK')

        print('date:', date, 'value:', value, 'currency:', currency, 'recipient:', recipient, 'account:', account, 'id:', accountId, 'notes:', notes, 'money:', money)

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

            try:
                money = Money(value, currency)
            except:
                money = Money(value, 'DKK')

            if date == transaction.date:
                date = ''
            if money == transaction.value:
                value = ''
            if recipient == transaction.recipient:
                recipient = ''
            if account == transaction.account.name or account == transaction.account.alias:
                account = ''
            if notes == transaction.notes:
                notes = ''

            if date != '' and date != None:
                transaction.date=date
            if value != '' and value != None:
                transaction.value=money
            if recipient != '' and recipient != None:
                transaction.recipient=recipient
            if account != '' and account != None:
                try:
                    account = Account.objects.get(name=account)
                    transaction.account = account
                except Account.DoesNotExist:
                    try:
                        account = Account.objects.get(alias=account)
                        transaction.account = account
                    except:
                        return render(req, 'Index.html', {'error': 'The account does not exist'})
            if notes != '' and notes != None:
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
    if req.method == 'POST':
        user = User.objects.get(username=req.user.username)
        data = json.loads(req.body)

        name = data['name']
        alias = data['alias']
        currency = data['currency']

        print('currency:', currency)
        try:
            Account.objects.get(name=name)
            return render(req, 'Index.html', {'error': 'The account already exists'})
        except Account.DoesNotExist:
            try:
                Account.objects.get(alias=alias)
                return render(req, 'Index.html', {'error': 'The account already exists'})
            except Account.DoesNotExist:
                money = None

                try:
                    money = Money(100, currency)
                except:
                    currency = 'DKK'
                    money = Money(100, currency)

                print('name:', name, 'alias:', alias, 'currency:', currency, 'money:', money)

                Account.objects.create(
                    user=user,
                    name=name,
                    alias=alias,
                    valuta=currency,
                )

                return redirect('home_page')
    else:
        return redirect('home_page')

def update_account(req):
    if req.method == 'POST':
        data = json.loads(req.body)

        try:
            account = Account.objects.get(id=data['id'])

            name = data['name']
            alias = data['alias']
            currency = data['currency']
            money = None
            
            if name == account.name:
                name = ''
            if alias == account.alias:
                alias = ''
            if currency == account.valuta:
                currency = ''

            if name != '' and name != None:
                account.name=name
            if alias != '' and alias != None:
                account.alias=alias
            if currency != '' and currency != None:
                try:
                    money = Money(100, currency)
                except:
                    currency = 'DKK'
                    money = Money(100, currency)
            
            print('id', data['id'], 'name:', name, 'alias:', alias, 'currency:', currency, 'money:', money)

            account.save()

        except Account.DoesNotExist:
            return render(req, 'Index.html', {'error': 'The account does not exist'})

        return redirect('home_page')
    else:
        return redirect('home_page')

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
                        user.is_staff = True  # Grant admin privileges
                        user.is_superuser = True  # Grant superuser privileges
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