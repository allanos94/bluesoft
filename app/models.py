from django.db import models
from django.contrib.auth.models import User
from app.choices import GenderChoices
from app.utils.generics import GeneralModel

from django.core.validators import MinValueValidator

GENDER_CHOICES = (
    ('M', 'Mujer'),
    ('H', 'Hombre'),
    ('O', 'Otro'),
)

class Client(GeneralModel):
    """ Client model for bank accounts """
    # User relationship
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Account relationship
    accounts = models.ManyToManyField('Account', related_name='clients')

    # Personal information
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    
    # Contact information
    phone_number = models.CharField(max_length=15)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    address = models.TextField()
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        """ Meta class for the Client model """
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
        db_table = 'clients'


class ClientType(GeneralModel):
    """ Client type model for bank accounts """
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50, null=True, blank=True)
    

    class Meta:
        """" Meta class for the ClientType model """
        verbose_name = 'Client Type'
        verbose_name_plural = 'Client Types'
        db_table = 'client_types'


class Account(GeneralModel):
    """ Account model for bank accounts """
    number = models.CharField(max_length=20, unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    account_type = models.ForeignKey('AccountType', on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'
        db_table = 'accounts'


class AccountType(GeneralModel):
    """ Account type model for bank accounts """
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50, null=True, blank=True)
    
    class Meta:
        """" Meta class for the AccountType model """
        verbose_name = 'Account Type'
        verbose_name_plural = 'Account Types'
        db_table = 'account_types'


# ------------------------------------------------------------ #

# Transaction model

class Transaction(GeneralModel):
    """ Transaction model for bank accounts """
    uuid = models.UUIDField()
    account = models.ForeignKey('Account', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    transaction_type = models.ForeignKey('TransactionType', on_delete=models.CASCADE)
    description = models.CharField(max_length=50, null=True, blank=True)
    target = models.ForeignKey('Account', on_delete=models.CASCADE, related_name='target_account', null=True, blank=True)
    
    class Meta:
        """ Meta class for the Transaction model """
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
        db_table = 'transactions'


class TransactionType(GeneralModel):
    """ Transaction type model for bank accounts """
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50, null=True, blank=True)
    
    class Meta:
        """" Meta class for the TransactionType model """
        verbose_name = 'Transaction Type'
        verbose_name_plural = 'Transaction Types'
        db_table = 'transaction_types'