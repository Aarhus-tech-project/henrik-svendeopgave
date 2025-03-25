from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import resolve, Resolver404
from .models import *
from djmoney.money import Money
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from djmoney.settings import CURRENCY_CHOICES

import json

VALID_CURRENCIES = {code for code, _ in CURRENCY_CHOICES}

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

def get_valid_money(value, currencies):
    for curr in currencies:
        try:
            return Money(value, curr)
        except:
            continue
    return None

@login_required
def add_transaction(req):
    if req.method != 'POST':
        return redirect('home_page')
    
    data = json.loads(req.body)
    date = data['date']
    value = round(float(data['value']), 2)
    currency = data.get('currency')
    recipient = data['recipient']
    account_id = data['id']
    notes = data['notes']

    try:
        account = Account.objects.get(id=account_id, user=req.user)
    except Account.DoesNotExist:
        return render(req, 'Index.html', {'error': 'The account does not exist'})

    currencies_to_try = [currency, account.valuta, 'DKK']
    money = get_valid_money(value, currencies_to_try)
    if money is None:
        return render(req, 'Index.html', {'error': 'No valid currency could be used'})
    
    Transaction.objects.create(
        user=req.user,
        date=date,
        value=money,
        recipient=recipient or '',
        account=account,
        notes=notes or '',
    )
    return redirect('home_page')

@login_required
def update_transaction(req):
    if req.method != 'POST':
        return redirect('home_page')
    
    data = json.loads(req.body)

    try:
        transaction = Transaction.objects.get(id=data['id'], user=req.user)
    except Transaction.DoesNotExist:
        return render(req, 'Index.html', {'error': 'The transaction does not exist'})
    
    date = data.get('date')
    value = data.get('value')
    currency = data.get('currency')
    recipient = data.get('recipient')
    account_name_or_alias = data.get('account')
    notes = data.get('notes')

    if date and date != transaction.date:
        transaction.date = date
    
    if value is not None:
        try:
            value = round(float(value), 2)
            currencies_to_try = [currency] if currency else []
            currencies_to_try.extend([transaction.value.currency, 'DKK'])
            money = get_valid_money(value, currencies_to_try)
            if money is None:
                return render(req, 'Index.html', {'error': 'No valid currency could be used'})
            transaction.value = money
        except (TypeError, ValueError):
            return render(req, 'Index.html', {'error': 'Invalid value provided'})

    if recipient and recipient != transaction.recipient:
        transaction.recipient = recipient
        
    if account_name_or_alias:
        try:
            account = Account.objects.get(
                Q(name=account_name_or_alias) | Q(alias=account_name_or_alias),
                user=req.user
            )
            transaction.account = account
        except Account.DoesNotExist:
            return render(req, 'Index.html', {'error': 'The account does not exist'})

    if notes and notes != transaction.notes:
        transaction.notes = notes

    transaction.save()
    return redirect('home_page')

@login_required
def delete_transaction(req):
    if req.method != 'POST':
        return redirect('home_page')
    
    data = json.loads(req.body)

    try:
        transaction = Transaction.objects.get(id=data['id'], user=req.user)
        transaction.delete()
    except Transaction.DoesNotExist:
        return render(req, 'Index.html', {'error': 'The transaction does not exist'})
    return redirect('home_page')

@login_required
def add_account(req):
    if req.method != 'POST':
        return redirect('home_page')
    
    data = json.loads(req.body)
    
    name = data['name']
    alias = data['alias']
    currency = data.get('currency')

    if Account.objects.filter(name=name, user=req.user).exists():
        return render(req, 'Index.html', {'error': 'The account name already exists'})
    if Account.objects.filter(alias=alias, user=req.user).exists():
        return render(req, 'Index.html', {'error': 'The account alias already exists'})
    
    if currency and currency not in VALID_CURRENCIES:
        currency = 'DKK'
    elif not currency or currency == '':
        currency = 'DKK'
    
    Account.objects.create(
        user=req.user,
        name=name,
        alias=alias,
        valuta=currency,
    )
    return redirect('home_page')

@login_required
def update_account(req):
    if req.method != 'POST':
        return redirect('home_page')
        
    data = json.loads(req.body)

    try:
        account = Account.objects.get(id=data['id'], user=req.user)
    except Account.DoesNotExist:
        return render(req, 'Index.html', {'error': 'The account does not exist'})
    
    name = data.get('name')
    alias = data.get('alias')
    currency = data.get('currency')

    if name and name != account.name:
        if Account.objects.filter(name=name, user=req.user).exists():
            return render(req, 'Index.html', {'error': 'The account name already exists'})
        account.name = name

    if alias and alias != account.alias:
        if Account.objects.filter(alias=alias, user=req.user).exists():
            return render(req, 'Index.html', {'error': 'The account alias already exists'})
        account.alias = alias

    if currency and currency != account.valuta:
        if currency not in VALID_CURRENCIES:
            return render(req, 'Index.html', {'error': 'Invalid currency provided'})
        account.valuta = currency
    
    account.save()
    return redirect('home_page')

@login_required
def delete_account(req):
    if req.method != 'POST':
        return redirect('home_page')
    
    data = json.loads(req.body)

    try:
        account = Account.objects.get(id=data['id'], user=req.user)
        account.delete()
    except Account.DoesNotExist:
        return render(req, 'Index.html', {'error': 'The account does not exist'})
    return redirect('home_page')

def login_view(req):
    if req.method != 'POST':
        return render(req, 'Login.html')

    data = json.loads(req.body)
    
    password = data.get('password')
    username_or_email = data.get('username_or_email')
    next_url = data.get('next_url', 'home_page')

    if not username_or_email or not password:
        return render(req, 'Login.html', {'error': 'Username/email and password are required'})

    try:
        user = User.objects.get(Q(username=username_or_email) | Q(email=username_or_email))
    except User.DoesNotExist:
        return render(req, 'Login.html', {'error': 'User does not exist'})
        
    if user.check_password(password):
        login(req, user)
        try:
            resolve(next_url)
            return redirect(next_url)
        except Resolver404:
            return redirect('home_page')
    return render(req, 'Login.html', {'error': 'Incorrect password'})

def signup_view(req):
    if req.method != 'POST':
        return render(req, 'Signup.html')
    
    data = json.loads(req.body)

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    confirm_password = data.get('confirm_password')
    next_url = data.get('next_url', 'home_page')

    if not all([username, email, password, confirm_password]):
        return render(req, 'Signup.html', {'error': 'All fields are required'})

    if User.objects.filter(username=username).exists():
        return render(req, 'Signup.html', {'error': 'Username already exists'})
    if User.objects.filter(email=email).exists():
        return render(req, 'Signup.html', {'error': 'Email already exists'})
    if password != confirm_password:
        return render(req, 'Signup.html', {'error': 'Passwords do not match'})
    
    user = User.objects.create_user(username=username, email=email, password=password)
    user.is_staff = True
    user.is_superuser = True
    user.save()

    authenticate_user = authenticate(req, username=username, password=password)

    if authenticate_user:
        login(req, authenticate_user)
        try:
            resolve(next_url)
            return redirect(next_url)
        except Resolver404:
            return redirect('home_page')
    return render(req, 'Login.html', {'error': 'Error during login from signup'})
    
@login_required
def update_user_view(req):
    if req.method != 'POST':
        return redirect('home_page')
    
    user = req.user
    data = req.POST

    username = data.get('username')
    email = data.get('email')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    password = data.get('password')
    confirm_password = data.get('confirm_password')

    if username and username != user.username:
        if User.objects.filter(username=username).exists():
            return render(req, 'Index.html', {'error': 'Username already exists', 'type': 'user'})
        user.username = username

    if email and email != user.email:
        if User.objects.filter(email=email).exists():
            return render(req, 'Index.html', {'error': 'Email already exists', 'type': 'user'})
        user.email = email

    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    if password and password == confirm_password:
        user.set_password(password)
    else:
        return render(req, 'Index.html', {'error': 'Passwords do not match', 'type': 'user'})

    user.save()
    return redirect('home_page')
        
@login_required
def delete_user_view(req):
    if req.method == 'POST':
        req.user.delete()
        logout(req)
        return redirect('home_page')
    return redirect('home_page')

def logout_view(req):
    logout(req)
    return redirect('login')