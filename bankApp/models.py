# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.utils.timezone
from django.contrib.auth.models import User
from django.db import models
import datetime

# Create your models here.
class Branch(models.Model):
    # Branch attributes
    name = models.CharField(max_length=20)
    country = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    phone = models.CharField(max_length=15)
    manager = models.CharField(max_length=20)

    # Return something meaningful
    def __str__(self):
        return '{} branch'.format(self.name) 

class BankRole(models.Model):
    #Bank role attributes
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class BankUser(models.Model):
    # This line is required. Links BankUser to a User model instance
    user = models.OneToOneField(User)
    # The additional attributes we wish to include
    middleName = models.CharField(max_length=20, blank=True)
    bankrole = models.ForeignKey(BankRole)
    branch = models.ForeignKey(Branch)
    
    # Return something meaningful
    def __str__(self):
        return '{} {} {}'.format(self.user.first_name,self.middleName,self.user.last_name)


class Customer(models.Model):
    # Customer attributes
    firstName = models.CharField(max_length=20)
    middleName = models.CharField(max_length=20, blank=True)
    lastName = models.CharField(max_length=20)
    address = models.CharField(max_length=20)
    email = models.CharField(max_length=20)
    mobile = models.CharField(max_length=20)
    sex = models.CharField(max_length=10)
    dateOfBirth = models.DateField(default= django.utils.timezone.now, blank=True, null=True)
    idNumber = models.IntegerField(default=0, blank=True)
    
    # Return something meaningful
    def __str__(self):
        return '{} {} {}'.format(self.firstName,self.middleName,self.lastName) 



class AccountType(models.Model):
    #Attributes of account type
    name = models.CharField(max_length=20)
    desc = models.TextField()

    # Return something meaningful
    def __str__(self):
        return self.name

class Account(models.Model):
    # Attributes of the account
    customer = models.OneToOneField(Customer,on_delete=models.CASCADE)
    accountType = models.ForeignKey(AccountType,default=1)
    branchOfReg = models.ForeignKey(Branch, blank=True)
    balance = models.IntegerField(default=0)

    # Return something meaningful
    def __str__(self):
        return '{} : {}'.format(self.id,self.customer) 

class Transactiontype(models.Model):
    name = models.CharField(max_length=20)

    # Return something meaningful
    def __str__(self):
        return self.name

class Transfer(models.Model):  
    sender = models.ForeignKey(Account,related_name='reciever')
    reciever = models.ForeignKey(Account,related_name='sender')

    # Return something meaningful
    def __str__(self):
        return '{} to {}'.format(self.sender,self.reciever)
    

class Transaction(models.Model):
    # Attributes of transaction
    bankUser = models.ForeignKey(BankUser,blank=True)
    account = models.ForeignKey(Account)
    Date = models.DateField(default=django.utils.timezone.now)
    amount = models.IntegerField()
    transactiontype = models.ForeignKey(Transactiontype)
    creditdebit = models.CharField(max_length=1)
    transfer  = models.ForeignKey(Transfer, on_delete=models.CASCADE,blank=True,default=0) 
    # Return something meaningful
    def __str__(self):
        return 'Account:{} _ trans:{}_amount:{}_time:{}'.format(self.account,self.transactiontype,self.amount,self.DateTime)


class JessSettings(models.Model):
    no_of_transactions_limit = models.IntegerField(default=5)
    rule_one_rank = models.IntegerField(default=20)
    rule_two_rank = models.IntegerField(default=20)
    rule_three_rank = models.IntegerField(default=20)
    


