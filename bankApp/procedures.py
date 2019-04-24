from .models import Transaction,Transactiontype
import datetime

def generateLimit(bankAccount,transID): 
    # Dyanamic generated limit
    # Get all withdraw transactions with the given bank account    
    transactions = Transaction.objects.filter(account = bankAccount).filter(transactiontype= transID)
    #Count all transactions for the given bank account    
    numOfTransactions = transactions.count()
    #Get the total amounts in the transaction    
    totalAmount = 0
    for transaction in transactions:
        totalAmount = totalAmount + transaction.amount
    
    # Get the average amount for all withdraw transactions 
    try:   
        averageAmount = totalAmount/numOfTransactions

    except ZeroDivisionError:
        averageAmount = 50000

    # Increment the average amount    
    increment = averageAmount * 1.5
    # We generate the new limit
    limit = averageAmount + increment    
    return limit

# Different checks whether the use performs a different 
# transaction on the same day
def generateDifferent(bankAccount,transID):
    Trans = Transactiontype.objects.get(pk=1)
    # All transactions for the bank Account today    
    today_filter = Transaction.objects.filter(account=bankAccount, DateTime=datetime.date.today()).exclude(transactiontype=Trans)
    
    if today_filter:
        different = "yes"
    
    else:
        different = "no"
    
    return different

# This function generates the number of transactions 
# per day                
def generateAverageNumberOfTrans(bankAccount,transID):
    numberOfTrans = Transaction.objects.filter(account=bankAccount, DateTime=datetime.date.today()).count()
    return numberOfTrans