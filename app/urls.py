from django.urls import path, include
from app import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    #AUTH
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    #USER REGISTER
    path('user_register/', views.UserRegisterView.as_view(), name='user_register'),
    #ACCOUNT BALANCE
    path('account_balance/', views.AccountBalanceView.as_view(), name='account_balance'),
    #TRANSACTIONS
    path('transaction/', views.TransactionsView.as_view(), name='transaction'),
]