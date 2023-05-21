from django.urls import path
from expenses import views

urlpatterns = [
    path("login/",views.LoginUser.as_view(),name='login'),
    path("register/",views.RegisterUser.as_view(),name='register'),
    path("profile/",views.GetProfile.as_view(),name='profile'),
    path("transaction/",views.ExpensesAPIView.as_view(),name='create'),
    path("balance/",views.BalanceAPIView.as_view(),name='balance'),
    path("totals/",views.TotalAPIView.as_view(),name='total'),
]