from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from django.db.models import Q

from app.models import Account, Client, Transaction
from app.serializers import AccountBalanceSerializer, ReadTransactionSerializer, UserRegisterSerializer, WriteTransactionSerializer

class UserRegisterView(APIView):
    """ This class is used to register a new user """
    serializer_class = UserRegisterSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"success": "User Account has been created Successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class AccountBalanceView(APIView):
    """ This class is used to get the account balance """
    serializer_class = AccountBalanceSerializer
    queryset = Client.objects.all().prefetch_related('accounts')
    
    def get(self, request):
        account_number = request.GET.get('account_number')
        if not account_number:
            accounts = self.queryset.get(user=request.user).accounts.all()
            serializer = self.serializer_class(accounts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        account = Account.objects.get(number=account_number, clients__user=request.user)
        serializer = self.serializer_class(account)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TransactionsView(generics.ListAPIView):
    """ This class is used to get the account transactions """
    queryset = Transaction.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ReadTransactionSerializer
        return WriteTransactionSerializer
    
    def get(self, request):
        account_number = request.GET.get('account_number')
        if not account_number:
            return Response({"error": "Account Number is required"}, status=status.HTTP_400_BAD_REQUEST)
        account = Account.objects.get(number=account_number, clients__user=request.user)
        transactions = self.queryset.filter(Q(origin=account) | Q(target=account))
        page = self.paginate_queryset(transactions)
        if page is not None:
            serializer = self.get_serializer_class()(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer_class()(transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = self.get_serializer_class()(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"success": "Transaction has been created Successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)