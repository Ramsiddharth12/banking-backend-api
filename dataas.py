import re
import random
from dbapp import db
from models import Customer,Transaction, Account, User


def phonenumber(phone):
        pattern= r"^\d{10}$"
        return bool(re.match(pattern,phone))

def AddCustomer(name,age,phone,balance,account_type):

    Valid_account=["savings","current"]

    if( name=="" or name is None or phone is None or age is None):
        return {"success":False, "Error":" you cant leave name, age, phone as empty "}
    
    if(not isinstance(age,int)):
        return ({"success":False, "Error":" age ahould only be in integer "})
    
    
    check=phonenumber(phone)

    if(not check):
        return ({"success":False, "Error":" please check and enter the correct phone number "})
    
    if (not isinstance(balance,(int,float))):
        return ({"success":False,"Error":" balance value should only be in integer / number"})
    
    if(account_type not in Valid_account):
        return ({"success":False,"Error":"The account type can only be <savings> or <current> "})
    
    while True:
            AccountN=random.randint(1000,9999)
            AccNo="28270100000"+str(AccountN)
            dupli=Account.query.filter_by(account_number=AccNo).first()
            if( not dupli):
                break
    try:
      create=Customer(name=name,age=age,phone=phone)
      db.session.add(create)
      db.session.flush()

      acc=Account(account_number=AccNo,account_type=account_type,balance=balance,customer_id=create.id)
      db.session.add(acc)
      db.session.flush()

      transaction=Transaction(action="Account Opening",amount=balance,balance_before=0,balance_after=balance,account_id=acc.id)
      db.session.add(transaction)
      db.session.commit()

      return ({"success":True, "Message":" A account for the customer is successfully created", "customer name":name, "account Number":AccNo ,"account type":account_type, "balance":balance })
    
    except Exception as e:
        db.session.rollback()
        return({"success":False, "Error":e})
    


def CreateAccount(name,phone,age,user_id):

    ExistingCustomer=Customer.query.filter_by(user_id=user_id).first()

    if(ExistingCustomer):
        return ({"success":False, "Error":" profile already exists "})

    if( name=="" or name is None or phone is None or age is None):
        return {"success":False, "Error":" you cant leave name, age, phone as empty "}
    
    if(not isinstance(age,int)):
        return ({"success":False, "Error":" age ahould only be in integer "})
    
    check=phonenumber(phone)

    if(not check):
        return ({"success":False, "Error":" please check and enter the correct phone number "})

    if(not isinstance(age,int)):
        return {"success":False,"Error":" please enter your correct age "}

    if(age<18 or age >100):
        return {"success":False,"Error":" not an valid age for account creation "}
    
    
    create=Customer(name=name,age=age,phone=phone,user_id=user_id)
    user=User.query.filter_by(id=user_id).first()
    db.session.add(create)
    db.session.flush()
    user.customer_id=create.id
    db.session.commit()
    return ({"success":True, "Message":" successfully created your profile", "customer name":name, "age":age ,"phone":phone})




def ActualAccountCreation(account_type, balance, identity):

    Valid_account=["savings","current"]

    if(account_type not in Valid_account):
        return ({"success":False,"Error":"The account type can only be <savings> or <current> "})    
    
    if (not isinstance(balance,(int,float))):
        return ({"success":False,"Error":" balance value should only be in integer / number"})
    
    if (balance<0):
        return ({"success":False,"Error":" balance must be greater than 0"})
    
    while True:
            AccountN=random.randint(1000,9999)
            AccNo="28270100000"+str(AccountN)
            dupli=Account.query.filter_by(account_number=AccNo).first()
            if( not dupli):
                break
    
    
    user=User.query.filter_by(id=identity).first()

    accounts=Account.query.filter_by(customer_id=user.customer_id).count()

    if(accounts>=5):
        return ({"success":False, "Error":" maximum amounts reached "})
    
    account=Account(account_number=AccNo, account_type=account_type, balance=balance, customer_id=user.customer_id)
    db.session.add(account)
    db.session.flush()
    transaction=Transaction(action="Account Opening",amount=balance,balance_before=0,balance_after=balance,account_id=account.id)
    db.session.add(transaction)
    db.session.commit()
    
    return ({"success":True, "Message":" Bank account has been created ", "account number":AccNo, "account_type":account_type ,"balance":balance})




def AccountClose(accno_last4,customerid,role):

    if(role=="admin"):
        account=Account.query.filter(Account.account_number.like(f"%{accno_last4}")).first()

        if(account is None):
            return ({"success":False, "Error":" please verify the account number "})

        Acc=account

        if(Acc.balance>0):
            return ({"success":False, "Error":" please withdraw all the amount from your account before closing the account"})
        
        db.session.delete(Acc)
        db.session.commit()       
        return({"success":True, "Customer account number":Acc.account_number,
            "Status": "The customer account and his transactions history are deleted from our system"})
    
    if(role=="customer"):
       account=Account.query.filter(Account.customer_id==customerid,Account.account_number.like(f"%{accno_last4}")).first()

       if(account is None):
            return ({"success":False, "Error":" please verify the account number "})
    
       Acc=account
       if(Acc.balance>0):
           return ({"success":False, "Error":" please withdraw all the amount from your account before closing the account"})  
     
    
       db.session.delete(Acc)
       db.session.commit()
       return({"success":True, "Customer account number":Acc.account_number,
            "Status": "The customer account and his transactions history are deleted from our system"})
    



def UpdateDetails(accno_last4,identity,role,name=None,phone=None,account_type=None,balance=None):

    if(role=="admin"):

        account=Account.query.filter(Account.account_number.like(f"%{accno_last4}")).first()

        if(account is None):
            return ({"success":False, "Error":" please verify the account number "})

        customer=Customer.query.get(account.customer_id)

        old_name=customer.name
        old_phone=customer.phone
        old_account_type=account.account_type
        old_balance=account.balance
    
        if(name):

           if(old_name==name):
              return ({"success":False, "Error":"the new name is same as the old name"})
        
           customer.name=name
    
        if(phone):
           
           if(old_phone==phone):
             return ({"success":False, "Error":"the new number is same as the old number"})
    
           check=phonenumber(phone)

           if(not check):
               return ({"success":False, "Error":" please check and enter the correct phone number "})
           
           customer.phone=phone

        if(account_type):
            Valid_account=["savings","current"]

            if(account_type not in Valid_account):
                return ({"success":False,"Error":"The account type can only be <savings> or <current> "})

            if(old_account_type==account_type):
               return ({"success":False, "Error":" account type was not changed "})
            
            account.account_type=account_type

        if(balance is not None):

            if (not isinstance(balance,(int,float))):
                return ({"success":False,"Error":" balance value should only be in integer / number"})
    
            if (balance<0):
                return ({"success":False,"Error":" balance must be greater than 0"})
            
            if(old_balance==balance):
                return ({"success":False, "Error":" balance was not changed "})
            
            account.balance=balance

        if (not any([name, phone, account_type, balance])):
           return {"success":False,"Error":"no update fields provided"}

        db.session.commit()
        return({"success":True, "Message":" customer details has been successfully updated"})
    

    if(role=="customer"):     
       customer=Customer.query.filter_by(user_id=identity).first()

       if (customer is None):
           return {"success":False,"Error":"customer profile not found"}

       account=Account.query.filter(Account.customer_id==customer.id,Account.account_number.like(f"%{accno_last4}")).first()

       if(account is None):
            return ({"success":False, "Error":" please verify the account number "})

       old_name=customer.name
       old_phone=customer.phone
    
       if(name):

          if(old_name==name):
             return ({"success":False, "Error":"the new name is same as the old name"})
        
          customer.name=name
    
       if(phone):
           
           if(old_phone==phone):
               return ({"success":False, "Error":"the new number is same as the old number"})
    
           check=phonenumber(phone)

           if(not check):
               return ({"success":False, "Error":" please check and enter the correct phone number "})
           
           customer.phone=phone
       
       if not any([name, phone]):
          return {"success":False,"Error":"no update fields provided"}

       db.session.commit()
       return({"success":True, "Message":" customer details has been successfully updated"})
    


def AccountFind(accno):

    if(accno is None or accno=="" or not accno):
        return {"success":False, "error_code":"LEFTEMPTY"}
    
    accounts=Account.query.all()
    match=[]

    for acc in accounts:
        if(acc.account_number.endswith(accno)):
            match.append(acc)

    if(len(match)==0):
       return {"success":False,"error_code":"NOTFOUND"}
    
    
    return ({"success": True, "account": match[0]})


def TransferErrorCodeCenter(error_code,role):

    ErrorsList={"LEFTEMPTY":f"you cant leave the {role} account number as empty", 
                "NOTFOUND":f"the {role} does not exist in our records"}
     
    return ({"success":False, "Error":ErrorsList.get(error_code)})