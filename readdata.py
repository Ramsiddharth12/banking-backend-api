import csv
from io import StringIO
from flask import Response
from datetime import datetime
from models import Customer,Transaction, Account, User

def ACustomer(customer_id): 
    
    accounts=[]
    acc=Account.query.filter_by(customer_id=customer_id).all()
    if (not acc):
        return ({"success":False, "Error":" no account found"})
    
    for ac in acc:
       accounts.append({"account number":ac.account_number, "account_type":ac.account_type, "balance":ac.balance})
    
    return({"success":True, "customer accounts":accounts})


def AllCustomers():
    result=[]
    users=User.query.all()

    for user in users:
        customer_data={"Email":user.email, "Role":user.role}

        if (user.customer_id):

            customers=Customer.query.get(user.customer_id)
            accounts=Account.query.filter_by(customer_id=customers.id).all()
            account_list=[]

            for acc in accounts:
                account_list.append({"account_number":acc.account_number, "account_type":acc.account_type, "balance":acc.balance})
            
            customer_data["Profile"]={"Name":customers.name, "age":customers.age, "phone":customers.phone}
            customer_data["accounts"]=account_list        

        result.append(customer_data)

    return ({"success":True,"customers":result})


def CheckBalance(customerId):
    
    accounts=Account.query.filter_by(customer_id=customerId).all()
    
    if(not accounts): 
        return ({"success":False, "Error":"No accounts found"})
    
    accounts_list=[]

    for acc in accounts:
        accounts_list.append({"account_number":acc.account_number, "balance":acc.balance})


    return({"success":True, "accounts and balance":accounts_list})
    

def AllTransactions():
     trans={}
     transaction=Transaction.query.all()
     accounts=Account.query.all()
     for acc in accounts:
         trans["account number"+" : "+acc.account_number]=[]
         for tran in transaction:
            if(tran.account_id==acc.id):
              trans["account number"+" : "+acc.account_number].append({"action":tran.action,"amount":tran.amount,"balance before":tran.balance_before,"balance after":tran.balance_after,"time stamp":tran.timestamp})

     return ({"success":True,"All transactions":trans})



def AllTransactionsOfASingleCustomer(CustomerId):
    
    accounts=Account.query.filter_by(customer_id=CustomerId).all()

    if(not accounts): 
        return ({"success":False, "Error":"No accounts found"})
    
    trans={}

    for acc in accounts:
       
       trans["account number" +" : "+acc.account_number]=[]
       transactions=Transaction.query.filter_by(account_id=acc.id).all()

       for tran in transactions:
            trans["account number" +" : "+acc.account_number].append({"action":tran.action,"amount":tran.amount,"balance before":tran.balance_before,
                                                                   "balance after":tran.balance_after,"time stamp":tran.timestamp})
    

    return ({"success":True,"Customers Transactions":trans})


def ExportTransactions(accno_last4,CustomerID,role):

    if(role!="customer"):
        return {"success":False, "Error":"Access denied"}

    account=Account.query.filter(Account.customer_id==CustomerID,Account.account_number.like(f"%{accno_last4}")).first()

    if(account is None):
        return ({"success":False, "Error":" please verify the account number "})
    
    transactions=Transaction.query.filter_by(account_id=account.id).all()

    output=StringIO()
    writer=csv.writer(output)
    writer.writerow(["Account Number","Action", "Amount", "Balance Before", "Balance After", "Time"])


    for transaction in transactions:
        writer.writerow([account.account_number,transaction.action,transaction.amount,transaction.balance_before,transaction.balance_after,transaction.timestamp])
    
    output.seek(0)

    filename=f"transactions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    return Response(output.getvalue(),mimetype="text/csv",headers={"Content-Disposition": f"attachment;filename={filename}"})

    

def AdminExport(role,value):
    
    if(role!="admin"):
        return {"success":False, "Error":"Access denied"}   

    Value_list=["customers","transactions","accounts"]

    if(value not in Value_list):
        return{"success":False, "Error":"Invalid-Action"}
    
    output=StringIO()
    writer=csv.writer(output)

    if(value=="customers"):
        customers=Customer.query.all()
        writer.writerow(["Name","Age","Phone"])
        for customer in customers:
            writer.writerow([customer.name,customer.age,customer.phone])
            filename=f"AllCustomers_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
    if(value=="accounts"):
        accounts=Account.query.all()
        writer.writerow(["Account Number","Account Type","Balance"])
        for account in accounts:
            writer.writerow([account.account_number,account.account_type,account.balance])
            filename=f"AllAccounts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    if(value=="transactions"):
        transactions=Transaction.query.all()
        writer.writerow(["Account Number","Action", "Amount", "Balance Before", "Balance After", "Time"])
        for transaction in transactions:
            accounts=Account.query.get(transaction.account_id)
            writer.writerow([accounts.account_number,transaction.action,transaction.amount,transaction.balance_before,transaction.balance_after,transaction.timestamp])
            filename=f"AllTransactions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    output.seek(0)
    return Response(output.getvalue(), mimetype="text/csv", headers={"Content-Disposition": f"attachment;filename={filename}"})