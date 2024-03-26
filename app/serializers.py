from rest_framework import serializers
from django.contrib.auth.models import User
from django.db import transaction
from babel.numbers import format_currency


from app.models import GENDER_CHOICES, Account, Client

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