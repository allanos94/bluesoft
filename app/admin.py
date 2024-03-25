from django.contrib import admin

from app.models import Account, AccountType, Client, ClientType, Transaction, TransactionType

admin.site.register(Account)
admin.site.register(AccountType)
admin.site.register(Client)
admin.site.register(ClientType)
admin.site.register(Transaction)
admin.site.register(TransactionType)