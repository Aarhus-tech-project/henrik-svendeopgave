from django.db import models
from django.contrib.auth.models import User
from encrypted_model_fields.fields import EncryptedCharField
from djmoney.models.fields import MoneyField, CurrencyField
from djmoney.money import Money
from djmoney.contrib.exchange.models import convert_money
from django.utils import timezone

def convert_function(value, currency):
    try:
        return convert_money(value, currency)
    except:
        STATIC_EXCHANGE_RATES = {
            'DKK': 1.0,
            'USD': 0.157,  # 1 DKK = 0.157 USD
            'EUR': 0.134,  # 1 DKK = 0.134 EUR
        }
        if currency in STATIC_EXCHANGE_RATES:
            new_value = value.amount * STATIC_EXCHANGE_RATES[currency]
            return Money(new_value, currency)
        else:
            raise ValueError(f"Currency {currency} not supported in STATIC_EXCHANGE_RATES")

# Create your models here.
class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = EncryptedCharField(max_length=255)
    alias = models.CharField(max_length=100, null=True, blank=True)
    valuta = CurrencyField(default='DKK')
    
    @property
    def get_transactions(self):
        transactions = self.transaction_set.all()
        converted_transactions = []
        for transaction in transactions:
            if transaction.value_currency != self.valuta:
                convertedValue = convert_function(transaction.value, self.valuta)
                transaction.value = convertedValue
            converted_transactions.append(transaction)
        return converted_transactions
    
    @property
    def get_total(self):
        transactions = self.get_transactions
        total = sum((transaction.value for transaction in transactions), Money(0, self.valuta))
        return total
    
class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(null=False, blank=False, default=timezone.now)
    value = MoneyField(max_digits=10, decimal_places=2, default_currency='DKK')
    recipient = models.CharField(max_length=255, null=True, blank=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    notes = models.CharField(max_length=1024, null=True, blank=True)

    @property 
    def get_rate(self):
        if self.value_currency != 'DKK':
            money = Money(100, self.value_currency)
            conversion_rate = convert_function(money, 'DKK')
            return conversion_rate

class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False, blank=False)
    value = MoneyField(max_digits=15, decimal_places=2, default_currency='DKK')
    buffer = MoneyField(max_digits=10, decimal_places=2, default_currency='DKK', null=True)
    date_added = models.DateField(auto_now_add=True, null=False, blank=False)
    goal_date = models.DateField(null=False, blank=False)
    notes = models.CharField(max_length=1024, null=True, blank=True)