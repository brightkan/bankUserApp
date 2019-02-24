# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render
from django.urls import reverse
from .models import AccountType,Customer,Account,Branch,Transaction,Transactiontype,BankUser
import datetime
import requests
import xml.etree.ElementTree as ET
# Create your views here.

def homePage(request):
    # The line requires the user to be authenticated before accessing the view responses. 
    if not request.user.is_authenticated:
        # if the user is not authenticated it renders a login page 
        return render(request,'bankApp/login.html',{"message":None})

    context = {
        "home":"active",
        "user":request.user
    }
    # If user is a manager
    user = request.user

    if str(user.bankuser.bankrole) == 'Manager':
        return render(request,"bankApp/manager/home.html", context)
    
    if str(user.bankuser.bankrole) == 'Teller':
        return render(request,"bankApp/teller/home.html",context)

    return HttpResponse("<h1>401 Error</h1> <br>User did not match any available bank roles")


def newCustomerPage(request):
    # The line requires the user to be authenticated before accessing the view responses. 
    if not request.user.is_authenticated:
        # if the user is not authenticated it renders a login page 
        return render(request,'bankApp/login.html',{"message":None})

    context = {
        "accountTypes":AccountType.objects.all(),
        "home":"active",
        "user":request.user
    }

    return render(request,"bankApp/manager/newCustomer.html",context)

def withdrawPage(request):
    # The line requires the user to be authenticated before accessing the view responses. 
    if not request.user.is_authenticated:
        # if the user is not authenticated it renders a login page 
        return render(request,'bankApp/login.html',{"message":None})

    context = {
        "withdraw":"active",
        "user":request.user
    }

    return render(request,"bankApp/teller/withdraw.html",context)


def depositPage(request):
    # The line requires the user to be authenticated before accessing the view responses. 
    if not request.user.is_authenticated:
        # if the user is not authenticated it renders a login page 
        return render(request,'bankApp/login.html',{"message":None})

    context = {
        "deposit":"active",
        "user":request.user
    }

    return render(request,"bankApp/teller/deposit.html",context)

def transferPage(request):
    # The line requires the user to be authenticated before accessing the view responses. 
    if not request.user.is_authenticated:
        # if the user is not authenticated it renders a login page 
        return render(request,'bankApp/teller/login.html',{"message":None})

    context = {
        "transfer":"active",
        "user":request.user
    }

    return render(request,"bankApp/teller/transfer.html",context)




        
# The login view authenticates the user
# The view also renders the login page
def login_view(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request,user)
        return HttpResponseRedirect(reverse('homePage'))
    
    else:
        return render(request, "bankApp/login.html", {"message":"Invalid credentials"})
        
    
# The logout view logs out the user
def logout_view(request):
    logout(request)
    return render(request, "bankApp/login.html", {"message":"Logged Out","info":"info"})


# Transaction logic
# The function below captures new customer details from the form and sends them to the database
def createCustomer(request):
    # The line requires the user to be authenticated before accessing the view responses. 
    if not request.user.is_authenticated:
        # if the user is not authenticated it renders a login page 
        return render(request,'bankApp/login.html',{"message":None})

    #This line requires a user to perform a POST request
    if request.method == 'POST':
        # Fetching data from the new customer form
        firstname = request.POST['firstName']
        middlename = request.POST['middleName']
        lastname = request.POST['lastName']
        address  =request.POST['address']
        email = request.POST['email']
        mobile = request.POST['mobile']
        sex = request.POST['sex']
        dob = request.POST['dob']
        accountType = int(request.POST['accountType'])
        
        try:
            # Creating instance of customer
            customer = Customer(firstName=firstname,middleName=middlename,lastName=lastname,address=address,email=email,mobile=mobile,sex=sex,dateOfBirth=dob)
            # Saving the customer instance to the database
            customer.save()
            
            # Getting the accountType instance submitted by the user 
            at = AccountType.objects.get(pk=accountType)
            
            # Getting the branch submitted by the user but we shall use one with primary key 1
            branch = Branch.objects.get(pk=1)

            # Creating a new instance of account
            account = Account(customer=customer,accountType=at,branchOfReg=branch)

            # Saving the account instance data to the database
            account.save()

            context = {
                "successmsg":"You have successfully created a bank account",
                "accountNumber":account.id,
                "name":"{} {} {}".format(customer.firstName,customer.middleName,customer.lastName),
                "accountType":at,
                "branch":branch
            }
            return render(request,'bankApp/manager/home.html',context)
        
        except:
            return render(request,'bankApp/manager/home.html',{"error":"Something went wrong"})
    
    return render(request,'bankApp/manager/home.html',{"error":"You have performed a get request"})



# Confirm withdraw
def confirmWithdraw(request):
    
    #This line requires a user to perform a POST request
    if request.method == 'POST':
       #Fetching data from the withdrawPage form 
       accountNumber = int(request.POST['accountNumber'])
       amount = int(request.POST['amount'])
       bankUserID = request.POST['bankUser']

       #Get the bank account object
       try:
           bankAccount = Account.objects.get(pk=accountNumber)

           context = {
           "url" : "initiateWithdraw",
           "type": "Withdraw",
           "bankUserId": bankUserID,
           "accountNumber": accountNumber,
           "amount":amount,
           "customerName": bankAccount.customer,
           "balance": bankAccount.balance,
           "customerMobile":bankAccount.customer.mobile,
           "customerSex": bankAccount.customer.sex,
           "accountType": bankAccount.accountType,
           "branchOfReg": bankAccount.branchOfReg,
           "Msg": "Are you sure you want to withdraw UGX {} from customer with customer details below?".format(amount)
            }
           
           return render(request, 'bankApp/teller/confirm.html', context)

       except Account.DoesNotExist:
            failedMsg = "The account number provided does not exist"
            context = {
            "failedMsg":failedMsg
                }   
            return render(request,"bankApp/teller/failed.html",context)

    #If the request method is not POST. Redirect the user back to the withdraw page  
    return HttpResponseRedirect(reverse('withdrawPage'))
       
       
#####################################################

# Withdraw Transaction logic

def initiateWithdraw(request):
    # The line requires the user to be authenticated before accessing the view responses. 
    if not request.user.is_authenticated:
        # if the user is not authenticated it renders a login page 
        return render(request,'bankApp/login.html',{"message":None})

    #This line requires a user to perform a POST request
    if request.method == 'POST':
       #Fetching data from the withdrawPage form 
       accountNumber = int(request.POST['accountNumber'])
       amount = int(request.POST['amount'])
       bankUserID = request.POST['bankUser']

       #Get the bank account object
       try:
           bankAccount = Account.objects.get(pk=accountNumber)

       except Account.DoesNotExist:
            failedMsg = "The account number provided does not exist"
            context = {
            "failedMsg":failedMsg
                }   
            return render(request,"bankApp/teller/failed.html",context)

       #Get the balance on the bank account
       balance = int(bankAccount.balance)
       #The Withdraw transaction processing
       if amount < balance:
           #Get Jess approval
           #Perform a post request to the server
           headers = {'Content-Type':'application/xml'}

           #Pass in the request data
           reqData = """<transaction><amount>{}</amount></transaction>""".format(amount)

           #Read the response data in xml
           try:
               resData = requests.post('http://localhost:8080/bankApp/rest/api',data=reqData, headers = headers).text.encode("utf-8")
               tree = ET.fromstring(resData)
               resMsg = tree.find('resMsg').text
               permit = tree.find('continue').text

           except:
               context = {
                   "failedMsg": "The application could not connect to the Jess engine"
               }
               return render(request,"bankApp/teller/failed.html",context)

           # permit determines whether the app should continue to commit the transaction 
           if permit == 'true': 
                #Perform the withdraw
                currentbalance = balance - amount
                #Update the current balance
                bankAccount.balance = currentbalance
                bankAccount.save()
                #Create a transaction object
                #Get a transaction of withdraw
                withdrawTrans = Transactiontype.objects.get(pk=1)
                bankUser = BankUser.objects.get(pk=bankUserID)
                transaction = Transaction(bankUser=bankUser, account=bankAccount,DateTime=datetime.date.today(),amount=amount,transactiontype=withdrawTrans, creditdebit=1)
                #Saving the transaction to the database
                transaction.save()
           
                #Setting a success message
                successMsg = 'You have successfully initiated the withdraw of UGX {}. The balance of account {} is UGX {}'.format(amount,bankAccount,bankAccount.balance)
                context = {
                  'successMsg': successMsg                     
                  }

                return render(request,"bankApp/teller/success.html",context)

           context = {
                "failedMsg":resMsg
            }

           return render(request,"bankApp/teller/failed.html",context)

        # If the amount is greater than the account balance
       failedMsg = "The account has insuficient balance"
       context = {
            "failedMsg":failedMsg
         }   
       return render(request,"bankApp/teller/failed.html",context)
        
    #If the request method is not POST. Redirect the user back to the withdraw page  
    return HttpResponseRedirect(reverse('withdrawPage'))

###################################################################################
# DEPOSIT LOGIC
def confirmDeposit(request):
    
    #This line requires a user to perform a POST request
    if request.method == 'POST':
       #Fetching data from the withdrawPage form 
       accountNumber = int(request.POST['accountNumber'])
       amount = int(request.POST['amount'])
       bankUserID = request.POST['bankUser']

       #Get the bank account object
       try:
           bankAccount = Account.objects.get(pk=accountNumber)

           context = {
           "url" : "initiateDeposit",
           "type": "Deposit",
           "bankUserId": bankUserID,
           "accountNumber": accountNumber,
           "amount":amount,
           "customerName": bankAccount.customer,
           "balance": bankAccount.balance,
           "customerMobile":bankAccount.customer.mobile,
           "customerSex": bankAccount.customer.sex,
           "accountType": bankAccount.accountType,
           "branchOfReg": bankAccount.branchOfReg,
           "Msg": "Are you sure you want to deposit UGX {} to the customer account with customer details below?".format(amount)
            }
           
           return render(request, 'bankApp/teller/confirm.html', context)

       except Account.DoesNotExist:
            failedMsg = "The account number provided does not exist"
            context = {
            "failedMsg":failedMsg
                }   
            return render(request,"bankApp/teller/failed.html",context)

    #If the request method is not POST. Redirect the user back to the withdraw page  
    return HttpResponseRedirect(reverse('depositPage'))

# Initiate the deposit transaction
def initiateDeposit(request):
    # The line requires the user to be authenticated before accessing the view responses. 
    if not request.user.is_authenticated:
        # if the user is not authenticated it renders a login page 
        return render(request,'bankApp/login.html',{"message":None})

    #This line requires a user to perform a POST request
    if request.method == 'POST':
       #Fetching data from the withdrawPage form 
       accountNumber = int(request.POST['accountNumber'])
       amount = int(request.POST['amount'])
       bankUserID = request.POST['bankUser']

       #Get the bank account object
       try:
           bankAccount = Account.objects.get(pk=accountNumber)

       except Account.DoesNotExist:
            failedMsg = "The account number provided does not exist"
            context = {
            "failedMsg":failedMsg
                }   
            return render(request,"bankApp/teller/failed.html",context)

       #Get the balance on the bank account
       balance = int(bankAccount.balance)
       #The Deposit transaction processing
      
       #Get Jess approval
       #Perform a post request to the server
       headers = {'Content-Type':'application/xml'}

       #Pass in the request data
       reqData = """<transaction><amount>{}</amount></transaction>""".format(amount)

       #Read the response data in xml
       try:
           resData = requests.post('http://localhost:8080/bankApp/rest/api',data=reqData, headers = headers).text.encode("utf-8")
           tree = ET.fromstring(resData)
           resMsg = tree.find('resMsg').text
           permit = tree.find('continue').text

       except:
           context = {
                "failedMsg": "The application could not connect to the Jess engine"
            }
           return render(request,"bankApp/teller/failed.html",context)

        # permit determines whether the app should continue to commit the transaction 
       if permit == 'true': 
           #Perform the deposit
           currentbalance = balance + amount
           #Update the current balance
           bankAccount.balance = currentbalance
           bankAccount.save()
           #Create a transaction object
           #Get a transactiontype object of deposit
           depositTrans = Transactiontype.objects.get(pk=2)
           bankUser = BankUser.objects.get(pk=bankUserID)
           transaction = Transaction(bankUser=bankUser, account=bankAccount,DateTime=datetime.date.today(),amount=amount,transactiontype=depositTrans, creditdebit=0)
           #Saving the transaction to the database
           transaction.save()
        
           #Setting a success message
           successMsg = 'You have successfully initiated the deposit of UGX {}. The balance of account {} is UGX {}'.format(amount,bankAccount,bankAccount.balance)
           context = {
                'successMsg': successMsg                     
                }

           return render(request,"bankApp/teller/success.html",context)

       context = {
            "failedMsg":resMsg
        }

       return render(request,"bankApp/teller/failed.html",context)

  
        
    #If the request method is not POST. Redirect the user back to the withdraw page  
    return HttpResponseRedirect(reverse('depositPage'))

##########################################################
# TRANSFER LOGIC
# Confirm transfer
def confirmTransfer(request):
    
    #This line requires a user to perform a POST request
    if request.method == 'POST':
       #Fetching data from the withdrawPage form 
       senderAccountNumber = int(request.POST['senderAccountNumber'])
       recieverAccountNumber = int(request.POST['recieverAccountNumber'])
       amount = int(request.POST['amount'])
       bankUserID = request.POST['bankUser']

       #Get the bank account objects
       try:
           
           senderAccount = Account.objects.get(pk=senderAccountNumber)
           recieverAccount = Account.objects.get(pk=recieverAccountNumber)
           reciever = {
               "name": recieverAccount.customer,
               "accountNumber": recieverAccount.id,
               "mobile": recieverAccount.customer.mobile,
               "sex": recieverAccount.customer.sex,
               "accountType": recieverAccount.accountType,
               "branchOfReg": recieverAccount.branchOfReg
           }
           context = {
           "url" : "initiateWithdraw",
           "type": "Transfer",
           "bankUserId": bankUserID,
           "accountNumber": senderAccount,
           "amount":amount,
           "customerName": senderAccount.customer,
           "balance": senderAccount.balance,
           "customerMobile":senderAccount.customer.mobile,
           "customerSex": senderAccount.customer.sex,
           "accountType": senderAccount.accountType,
           "branchOfReg": senderAccount.branchOfReg,
           "reciever": reciever,
           "Msg": "Are you sure you want to transfer UGX {} from customer to account with details below?".format(amount)
            }
           
           return render(request, 'bankApp/teller/confirm.html', context)

       except Account.DoesNotExist:
            failedMsg = "One of the account numbers provided does not exist"
            context = {
            "failedMsg":failedMsg
                }   
            return render(request,"bankApp/teller/failed.html",context)

    #If the request method is not POST. Redirect the user back to the withdraw page  
    return HttpResponseRedirect(reverse('transferPage'))


def initiateTransfer(request):
    # The line requires the user to be authenticated before accessing the view responses. 
    if not request.user.is_authenticated:
        # if the user is not authenticated it renders a login page 
        return render(request,'bankApp/login.html',{"message":None})

    #This line requires a user to perform a POST request
    if request.method == 'POST':
       #Fetching data from the withdrawPage form 
       senderAccountNumber = int(request.POST['senderAccountNumber'])
       recieverAccountNumber = int(request.POST['recieverAccountNumber'])
       amount = int(request.POST['amount'])
       bankUserID = request.POST['bankUser']

       #Get the bank account object
       try:
           senderAccount = Account.objects.get(pk=senderAccountNumber)
           recieverAccount = Account.objects.get(pk=recieverAccountNumber)

       except Account.DoesNotExist:
            failedMsg = "The account number provided does not exist"
            context = {
            "failedMsg":failedMsg
                }   
            return render(request,"bankApp/teller/failed.html",context)

       #Get the balance on the sender's bank account
       senderbalance = int(senderAccount.balance)
       recieverbalance = int(recieverAccount.balance)
       #The Transfer transaction processing
       if amount < senderbalance:
           #Get Jess approval
           #Perform a post request to the server
           headers = {'Content-Type':'application/xml'}

           #Pass in the request data
           reqData = """<transaction><amount>{}</amount></transaction>""".format(amount)

           #Read the response data in xml
           try:
               resData = requests.post('http://localhost:8080/bankApp/rest/api',data=reqData, headers = headers).text.encode("utf-8")
               tree = ET.fromstring(resData)
               resMsg = tree.find('resMsg').text
               permit = tree.find('continue').text

           except:
               context = {
                   "failedMsg": "The application could not connect to the Jess engine"
               }
               return render(request,"bankApp/teller/failed.html",context)

           # permit determines whether the app should continue to commit the transaction 
           if permit == 'true': 
                #Perform the transfer
                senderbalance = senderbalance - amount
                recieverbalance = recieverbalance + amount
                #Update the senders balance
                senderAccount.balance = senderbalance
                senderAccount.save()
                #Update the recievers balance
                recieverAccount.balance = recieverbalance
                recieverAccount.save()
                #Create a transaction object
                #Get a transaction of withdraw
                transferTrans = Transactiontype.objects.get(pk=3)
                bankUser = BankUser.objects.get(pk=bankUserID)
                # Create send transaction
                sendertransaction = Transaction(bankUser=bankUser, account=senderAccount,DateTime=datetime.date.today(),amount=amount,transactiontype=transferTrans, creditdebit=1)
                #Saving the transaction to the database
                sendertransaction.save()
                # Create recieve transaction
                recievertransaction = Transaction(bankUser=bankUser, account=recieverAccount,DateTime=datetime.date.today(),amount=amount,transactiontype=transferTrans, creditdebit=0)
                #Saving the transaction to the database
                recievertransaction.save()
           
                #Setting a success message
                successMsg = 'You have successfully initiated the transfer of  UGX {} from {} to {}. The balance of account {} is UGX {}'.format(amount,senderAccount,recieverAccount,senderAccount,senderAccount.balance)
                context = {
                  'successMsg': successMsg                     
                  }

                return render(request,"bankApp/teller/success.html",context)

           context = {
                "failedMsg":resMsg
            }

           return render(request,"bankApp/teller/failed.html",context)

        # If the amount is greater than the account balance
       failedMsg = "The sender's account has insuficient balance"
       context = {
            "failedMsg":failedMsg
         }   
       return render(request,"bankApp/teller/failed.html",context)
        
    #If the request method is not POST. Redirect the user back to the withdraw page  
    return HttpResponseRedirect(reverse('withdrawPage'))
       
    

        
        
            

        
           
           
            
            

     





   
