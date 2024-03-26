from rest_framework import serializers
from django.contrib.auth.models import User
from django.db import transaction
from babel.numbers import format_currency


from app.models import GENDER_CHOICES, Account, Client, Transaction, TransactionType

class UserRegisterSerializer(serializers.Serializer):
    """ This class is used to serialize the user registration data """
    # User Data
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    # Client Data
    date_of_birth = serializers.DateField()
    gender = serializers.ChoiceField(choices=GENDER_CHOICES)
    phone_number = serializers.CharField()
    state = serializers.CharField()
    city = serializers.CharField()
    address = serializers.CharField()
    # Account Data
    account_type = serializers.CharField()
    
    def create(self, validated_data):
        with transaction.atomic():
            create_user = CreateUserSerializer(data=validated_data)
            create_user.is_valid(raise_exception=True)
            create_user.save()

            validated_data["user"] = create_user.data["id"]
            create_client = CreateClientSerializer(data=validated_data)
            create_client.is_valid(raise_exception=True)
            new_client = create_client.save()
            
            validated_data["client"] = create_client.data["id"]
            create_account = CreateAccountSerializer(data=validated_data)
            create_account.is_valid(raise_exception=True)
            new_account = create_account.save()
            
            #Ad account to client
            new_client.accounts.add(new_account)
            return create_user



class CreateUserSerializer(serializers.ModelSerializer):
    """ This class is used to serialize the user registration data """
    
    def create(self, validated_data):
        create_user = User.objects.create_user(**validated_data)
        return create_user
    class Meta:
        model = User
        fields = '__all__'


class CreateClientSerializer(serializers.ModelSerializer):
    """ This class is used to serialize the client registration data """
    
    def create(self, validated_data):
        create_client = Client.objects.create(**validated_data)
        return create_client

    class Meta:
        model = Client
        fields = '__all__'


class CreateAccountSerializer(serializers.ModelSerializer):
    """ This class is used to serialize the account registration data """
    number = serializers.CharField(required=False)
    
    def create(self, validated_data):
        create_account = Account.objects.create(**validated_data)
        return create_account

    class Meta:
        model = Account
        fields = '__all__'


class AccountBalanceSerializer(serializers.ModelSerializer):
    """ This class is used to serialize the account balance data """
    balance = serializers.SerializerMethodField()
    number = serializers.CharField()
    
    
    def get_balance(self, obj):
        return format_currency(obj.balance, 'COP', locale='es_CO')


    class Meta:
        model = Account
        fields = ['number', 'balance']
        
class ReadTransactionSerializer(serializers.ModelSerializer):
    """ This class is used to serialize the read transaction data """
    amount = serializers.SerializerMethodField()
    transaction_type = serializers.CharField()
    target = serializers.CharField()
    description = serializers.CharField()
    
    def get_amount(self, obj):
        return format_currency(obj.amount, 'COP', locale='es_CO')
    
    class Meta:
        model = Transaction
        fields = '__all__'


class WriteTransactionSerializer(serializers.Serializer):
    """ This class is used to serialize the write transaction data """
    origin = serializers.CharField(required=False)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = serializers.CharField()
    target = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    
    def validate(self, attrs):
        transactions_choices = TransactionType.objects.values_list('name', flat=True)
        transaction_type = attrs.get('transaction_type')
        if transaction_type not in transactions_choices:
            raise serializers.ValidationError("Invalid transaction type")
        if transaction_type in ['Transferencia', 'Consignación'] and not attrs.get('target'):
            raise serializers.ValidationError("Target account is required for transfer or deposit transactions")
        if transaction_type == 'Retiro' and not attrs.get('origin'):
            raise serializers.ValidationError("Origin account is required for withdrawal transactions")                
        return attrs

    def create(self, validated_data):
        with transaction.atomic():
            transaction_type = TransactionType.objects.get(name=validated_data.get('transaction_type'))   
            origin = Account.objects.filter(number=validated_data.get('origin')).first()
            target = Account.objects.filter(number=validated_data.get('target')).first()
            amount = validated_data.get('amount')
            if transaction_type.name == 'Transferencia':
                if origin.balance < amount:
                    raise serializers.ValidationError({"error": "Origin account does not have enough balance"})
                origin.balance -= amount
                target.balance += amount
            elif transaction_type.name == 'Consignación':
                target.balance += amount
            elif transaction_type.name == 'Retiro':
                if origin.balance < amount:
                    raise serializers.ValidationError({"error": "Origin account does not have enough balance"})
                origin.balance -= amount
            origin.save() if origin else None
            target.save() if target else None
            validated_data['origin'] = origin
            validated_data['target'] = target
            validated_data['amount'] = amount
            validated_data['transaction_type'] = transaction_type
            create_transaction = Transaction.objects.create(**validated_data)
            return create_transaction