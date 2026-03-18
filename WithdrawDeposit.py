from dbapp import db
from models import Transaction, Account
from dataas import AccountFind, TransferErrorCodeCenter


class deposit_withdraw():
   
   def __init__(self,accno_last4,deposit_amount,withdraw_amount,CustomerId): 
       self.accno_last4=accno_last4
       self.deposit_amount=deposit_amount
       self.withdraw_amount=withdraw_amount
       self.customer_id=CustomerId

   def deposit(self):
    
    if(self.accno_last4=="" or self.accno_last4 is None or not self.accno_last4):
        return {"success":False, "Error":"you cant leave the accno as empty"}

    if (not isinstance (self.deposit_amount,(int,float)) or self.deposit_amount is None):
       return {"success": False, "Error": "deposit-amount value should only be an integer / number"}

    if (self.deposit_amount<=0):
       return {"success": False, "Error": "Invalid deposit amount"}
    
    account=Account.query.filter(Account.customer_id==self.customer_id,Account.account_number.like(f"%{self.accno_last4}")).first()
    
    if(not account):
        return {"success":False, "Error":"Incorrect account number"}
   
    
    try:
        oldbalance=account.balance
        
        db.session.begin()
        account.balance+=self.deposit_amount
        dep=Transaction(action="Deposit",amount=self.deposit_amount, balance_before=oldbalance,balance_after= account.balance,account_id=account.id)
        db.session.add(dep)
        db.session.commit()
               
        return ({"success":True, "Message":"Amount has been successfully deposited", "customer accont number":account.account_number,
                     "updated Balance":account.balance})
    
    except Exception as e:
        db.session.rollback()
        return ({"success":False,"Error":e})
 
         
   def withdraw(self):


    if(self.accno_last4=="" or self.accno_last4 is None or not self.accno_last4):
        return {"success":False, "Error":"you cant leave the accno as empty"}
   
    if (not isinstance (self.withdraw_amount,(int,float)) or self.withdraw_amount is None):
       return {"success": False, "Error": "withdraw-amount value should only be an integer / number"}

    if(self.withdraw_amount<=0):
        return ({"success": False, "Error": "Invalid withdraw amount"})
    
    account=Account.query.filter(Account.customer_id==self.customer_id,Account.account_number.like(f"%{self.accno_last4}")).first()
    
    if(not account):
        return {"success":False, "Error":"Incorrect account number"}

    if(account.balance<self.withdraw_amount):
           return({"success":False, "Error":"the entered amount is higher than your balance",
                   "Message":"enter a amount within your bank balance"})
    
    try:
        oldbalance=account.balance
        
        db.session.begin()
        account.balance-=self.withdraw_amount
        With=Transaction(action="Withdraw",amount= self.withdraw_amount, balance_before=oldbalance,balance_after=account.balance,account_id=account.id)
        db.session.add(With)
        db.session.commit()
                
        return ({"success":True, "Message":"Amount has been successfully withdrawn", "customer accont number":account.account_number,
                     "updated Balance":account.balance})
          
    except Exception as e:
        db.session.rollback()
        return ({"success":False,"Error":e})
                  
    
class TransferAmounts():
    def __init__(self,sender,receiver,amount):
        self.sender=sender
        self.receiver=receiver
        self.amount=amount

    def transfer(self):
     acc1=AccountFind(self.sender)
     acc2=AccountFind(self.receiver)
         
    
     if(not acc1["success"]):
             
         return TransferErrorCodeCenter(acc1["error_code"],"sender")
         
                     
     if(not acc2["success"]):
             
         return TransferErrorCodeCenter(acc2["error_code"],"receiver")                 


     if(not isinstance(self.amount,(int,float))):
        return ({"success":False, "Error":"amount to be transferred value should only be an integer/number"})  
        
     if(self.amount<=0):
            return ({"success": False, "Error": "Invalid amount cant process transfer"})
         

     account1=acc1["account"]
     account2=acc2["account"]

     if(account1.balance<self.amount):
        return({"success":False, "Error":"the entered amount is higher than sender bank balance",
                               "Message":"enter a amount within the bank balance"})

     if(account1.account_number==account2.account_number):
        return ({"success":False, "Error":"the sender and receiver are same accounts cant process transactions"})

        
     try:
        acc1oldbalance=account1.balance
        acc2oldbalance=account2.balance

        db.session.begin()
        account1.balance-=self.amount
        account2.balance+=self.amount
        transfer1=Transaction(action="Transfer Out",amount= self.amount, balance_before=acc1oldbalance,balance_after=account1.balance,account_id=account1.id)
            
        transfer2=Transaction(action="Transfer In",amount= self.amount, balance_before=acc2oldbalance,balance_after=account2.balance,account_id=account2.id)
        db.session.add_all([transfer1,transfer2])
        db.session.commit()
                    
        return({"success":True, "Message":"Transaction is successful", "Sender accont number":account1.account_number, "Sender Updated Balance":account1.balance
                                    ,"Receiver accont number":account2.account_number, "Receiver Updated Balance":account2.balance}) 
    
     except Exception as e:
        db.session.rollback()
        return({"success":False,"Error":e})