# Generated by Django 5.0.3 on 2024-03-26 16:42

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'verbose_name': 'Account Type',
                'verbose_name_plural': 'Account Types',
                'db_table': 'account_types',
            },
        ),
        migrations.CreateModel(
            name='ClientType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'verbose_name': 'Client Type',
                'verbose_name_plural': 'Client Types',
                'db_table': 'client_types',
            },
        ),
        migrations.CreateModel(
            name='TransactionType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'verbose_name': 'Transaction Type',
                'verbose_name_plural': 'Transaction Types',
                'db_table': 'transaction_types',
            },
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('number', models.CharField(max_length=20, unique=True)),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('account_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.accounttype')),
            ],
            options={
                'verbose_name': 'Account',
                'verbose_name_plural': 'Accounts',
                'db_table': 'accounts',
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('date_of_birth', models.DateField()),
                ('gender', models.CharField(choices=[('M', 'Mujer'), ('H', 'Hombre'), ('O', 'Otro')], max_length=10)),
                ('phone_number', models.CharField(max_length=15)),
                ('state', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('address', models.TextField()),
                ('accounts', models.ManyToManyField(blank=True, related_name='clients', to='app.account')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Client',
                'verbose_name_plural': 'Clients',
                'db_table': 'clients',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('uuid', models.UUIDField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0.01)])),
                ('description', models.CharField(blank=True, max_length=50, null=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.account')),
                ('target', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='target_account', to='app.account')),
                ('transaction_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.transactiontype')),
            ],
            options={
                'verbose_name': 'Transaction',
                'verbose_name_plural': 'Transactions',
                'db_table': 'transactions',
            },
        ),
    ]
