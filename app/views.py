from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from app.models import Account, Client
from app.serializers import AccountBalanceSerializer, UserRegisterSerializer

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
    permission_classes = [IsAuthenticated]
    queryset = Client.objects.all().prefetch_related('accounts')
    
    def get(self, request):
        account_number = request.GET.get('account_number')
        if not account_number:
            accounts = self.queryset.get(user=request.user).accounts.all()
            serializer = self.serializer_class(accounts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)