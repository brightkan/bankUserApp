# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import Branch,BankUser,BankRole,Customer,Account,AccountType,Transaction,Transactiontype,Transfer,JessSettings
# Register your models here.

admin.site.register(Branch)
admin.site.register(BankUser)
admin.site.register(BankRole)
admin.site.register(Customer)
admin.site.register(Account)
admin.site.register(AccountType)
admin.site.register(Transaction)
admin.site.register(Transactiontype)
admin.site.register(Transfer)
admin.site.register(JessSettings)