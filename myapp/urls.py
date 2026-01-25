"""
URL configuration for bankProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views

app_name = 'myapp'
urlpatterns = [
   path('',views.starting_page,name="starting_page"),
   path('createAccount/',views.CreatePage,name="create"),
   path('accountNumber/<int:account_num>/',views.showAccountNum,name="accountNum"),
   path('main/<int:customer_id>/',views.mainPage,name="mainPage"),
   path('login/',views.loginPage,name="login"),
   path('checkbalance/<str:account_no>/',views.checkBalance,name="checkBalance"),
   path('deposit/<str:account_no>/',views.deposit,name="deposit"),
   path('upi/<str:account_no>/',views.upi,name="upi"),
   path('transaction/<str:account_no>/',views.transaction,name="transaction"),
   path('update/<str:account_no>/',views.update,name="update"),
   path('delete/<str:account_no>',views.delete,name='delete'),
   path('billpayments/<str:account_no>',views.bill_payments,name='bill_payments'),
   path('loan/<str:account_no>',views.loan_given,name='loan'),
   path('loan_details/<str:account_no>',views.loan_details_table,name='loan_details_table'),
   path('loan_details/pay_loan/<str:refno>/<str:account_no>',views.pay_loan,name='pay_loan'),
]
