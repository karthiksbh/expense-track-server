from django.urls import path
from expenses import views

urlpatterns = [
    path("login/",views.LoginUser.as_view(),name='login'),
    path("register/",views.RegisterUser.as_view(),name='register'),
    path("profile/",views.GetProfile.as_view(),name='profile'),
    path("transaction/",views.ExpensesAPIView.as_view(),name='create'),
    path("balance/",views.BalanceAPIView.as_view(),name='balance'),
    path("totals/",views.TotalAPIView.as_view(),name='total'),
    path("history/",views.HistoryAPIView.as_view(),name='history'),
    path("delete/<int:id>/",views.DeleteTransaction.as_view(),name='delete'),
    path("income-wise/",views.IncomeGroupWise.as_view(),name='incomewise'),
    path("expense-wise/",views.ExpenseGroupWise.as_view(),name='incomewise'),
]