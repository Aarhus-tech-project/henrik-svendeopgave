# Generated by Django 5.1.6 on 2025-03-18 09:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0007_alter_transaction_recipient'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='valuta',
        ),
    ]
