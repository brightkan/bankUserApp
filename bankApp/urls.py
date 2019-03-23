from django.conf.urls import url
from django.contrib import admin
from . import views
urlpatterns = [
    url(r'^$', views.homePage, name='homePage'),
    url(r'^newCustomer$', views.newCustomerPage, name='newCustomer'),
    url(r'^withdraw$', views.withdrawPage, name='withdrawPage'),
    url(r'^deposit$', views.depositPage, name='depositPage'),
    url(r'^transfer$', views.transferPage, name='transferPage'),
    url(r'^login$', views.login_view, name='login'),
    url(r'^logout$', views.logout_view, name='logout'),
    url(r'^createCustomer$', views.createCustomer, name='createCustomer'),
    url(r'^initiateWithdraw$', views.initiateWithdraw, name='initiateWithdraw'),
    url(r'^confirmWithdraw$', views.confirmWithdraw, name='confirmWithdraw'),
    url(r'^confirmDeposit$', views.confirmDeposit, name='confirmDeposit'),
    url(r'^initiateDeposit$', views.initiateDeposit, name='initiateDeposit'),
    url(r'^confirmTransfer$', views.confirmTransfer, name='confirmTransfer'),
    url(r'^initiateTransfer$', views.initiateTransfer, name='initiateTransfer'),
    url(r'^customers$', views.customersPage, name='customersPage'),
    url(r'^tellers$', views.tellersPage, name='tellersPage'),
    url(r'^newTeller$', views.newTeller, name='newTeller'),
    url(r'^createTeller$', views.createTeller, name='createTeller'),
]