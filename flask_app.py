import os
from dbapp import db
from flask import Flask,jsonify,request
from auth import registering,logingin
from WithdrawDeposit import deposit_withdraw,TransferAmounts
from flask_jwt_extended import JWTManager, jwt_required, get_jwt, get_jwt_identity
from dataas import AddCustomer,AccountClose,UpdateDetails, CreateAccount , ActualAccountCreation, ExportTransactions, AdminExport
from readdata import ACustomer,AllCustomers,AllTransactionsOfASingleCustomer,CheckBalance,AllTransactions



app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///bank.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.config["JWT_SECRET_KEY"]=os.getenv("JWT_SECRET_KEY")
db.init_app(app)
jwt=JWTManager(app)


@app.route("/")
def home():
    return jsonify({"success":True, "Message":"hello its started huh"}),200



@app.route("/register",methods=["POST"])
def registration():
    data=request.get_json()

    regi=registering(data.get("email"), data.get("password"), role="customer") 
    
    return (jsonify(regi), 201) if regi["success"] else (jsonify(regi), 400)




@app.route("/login",methods=["POST"])
def login():
    data=request.get_json()
    email=data.get("email")
    password=data.get("password")
    log=logingin(email,password)

    if (not email or not password ):
        return ({"success":False, "Error":" Email and password required "}),400
    
    return (jsonify(log), 200) if log["success"] else (jsonify(log), 401)


@app.route("/createprofile",methods=["POST"])
@jwt_required()
def profilecreation():
    clamis=get_jwt()
    Role=clamis.get("role")

    if (Role!="customer"):
        return jsonify({"success":False, "Error":"Access denied"}),403
    
    user_id=get_jwt_identity()
    
    data=request.get_json()
    name=data.get("name")
    age=data.get("age")
    phone=data.get("phone")

    create=CreateAccount(name,phone,age,user_id)
    return (jsonify(create),200) if create["success"] else (jsonify(create),400)



@app.route("/createaccount", methods=["POST"])
@jwt_required()
def accountcreation():
    claims=get_jwt()
    Role=claims.get("role")
    identity=get_jwt_identity()

    if (Role!="customer"):
        return jsonify({"success":False, "Error":"Access denied"}),403
    
    data=request.get_json()

    acc=ActualAccountCreation(data.get("account_type"), data.get("balance"), identity)
    return (jsonify(acc),201) if acc["success"] else (jsonify (acc),400)



@app.route("/addcustomer",methods=["POST"])
@jwt_required()
def AddCustomerDetails():

    claims=get_jwt()
    Role=claims.get("role")
    if (Role!="admin"):
        return jsonify({"success":False, "Error":"Access denied"}),403

    data=request.get_json()
    name=data.get("name")
    age=data.get("age")
    phone=data.get("phone")  
    balance=data.get("balance")
    account_type=data.get("account_type")

    cust=AddCustomer(name,age,phone,balance,account_type)

    return (jsonify(cust), 201) if cust["success"] else (jsonify(cust), 500)


@app.route("/AccountClose/<accno_last4>",methods=["DELETE"])
@jwt_required()
def AccountDeletion(accno_last4):
    claims=get_jwt()
    customerid=claims.get("customer_id")
    role=claims.get("role")
    if(len(accno_last4)==4):
      close=AccountClose(accno_last4,customerid,role)
      return (jsonify(close), 200) if close["success"] else (jsonify(close), 404)
    return jsonify({"success":False, "Error":" please enter only the last -4 digits- of the account number"}),400

    

@app.route("/Changedetails/<accno_last4>",methods=["PUT"])
@jwt_required()
def ChangeName(accno_last4):

    claims=get_jwt()
    identity=get_jwt_identity()
    role=claims.get("role")
    data=request.get_json()
    if(len(accno_last4)==4):
        result=UpdateDetails(accno_last4,identity,role, data.get("name"), data.get("phone"), data.get("account_type"), data.get("balance"))
        return (jsonify(result), 200) if result["success"] else (jsonify(result), 404)
    
    return jsonify({"success":False, "Error":" please enter only the last -4 digits- of the account number"}),400   



@app.route("/customerdetail")
@jwt_required()
def ACustomerDetails():
    claims=get_jwt()
    role=claims.get("role")

    if (role=="admin"):
        return jsonify({"success":False, "Error":"Access denied"}),403
    
    customer_id=claims.get("customer_id")
    cust=ACustomer(customer_id)
    return (jsonify(cust), 200) if cust["success"] else (jsonify(cust), 404) 


@app.route("/allcustomersdetails")
@jwt_required()
def AllCustomer():
    claims=get_jwt()
    role=claims.get("role")

    if (role!="admin"):
        return jsonify({"success":False, "Error":"Access denied"}),403
    
    allcust=AllCustomers()

    return (jsonify(allcust), 200) if allcust["success"] else (jsonify(allcust), 404)



@app.route("/balance")
@jwt_required()
def Balance():
    claims=get_jwt()
    role=claims.get("role")
    customerId=claims.get("customer_id")
    
    if (role!="customer"):
        return jsonify({"success":False, "Error":"Access denied"}),403

    
    balance=CheckBalance(customerId)
    return (jsonify(balance), 200) if balance["success"] else (jsonify(balance), 403)
    

@app.route("/transactions")
@jwt_required()
def ALLTransactions():
    claims=get_jwt()
    role=claims.get("role")

    if(role!="admin"):
        return jsonify({"success":False, "Error":"Access denied"}),403
      
    AllT=AllTransactions()

    return (jsonify(AllT), 200) if AllT["success"] else (jsonify(AllT), 404)


@app.route("/SingleCustomerTransactions")
@jwt_required()
def SingleCustTrans():
    claims=get_jwt()
    Role=claims.get("role")
    CustomerId=claims.get("customer_id")

    if (Role!="customer"):
        return jsonify({"success":False, "Error":"Access denied"}),403

    STran=AllTransactionsOfASingleCustomer(CustomerId)
    return (jsonify(STran), 200) if STran["success"] else (jsonify(STran), 404)


@app.route("/transaction/export/<accno_last4>")
@jwt_required()
def downloadcsv(accno_last4):
    claims=get_jwt()
    role=claims.get("role")
    customerID=claims.get("customer_id")
    
    if(len(accno_last4)==4):
        return ExportTransactions(accno_last4,customerID,role)

    return jsonify({"success":False, "Error":" please enter only the last -4 digits- of the account number"}),400

@app.route("/admin/export/<value>")
@jwt_required()
def Downloadcsv(value):
    claims=get_jwt()
    role=claims.get("role")
    return AdminExport(role,value)



@app.route("/deposit",methods=["POST"])
@jwt_required()
def Deposit():
    claims=get_jwt()
    role=claims.get("role")
    CustomerId=claims.get("customer_id")

    if(role!="customer"):
        return jsonify({"success":False, "Error":"Access denied"}),403

    data=request.get_json()
    accno_last4=data.get("accno_last4")
    deposit_amount=data.get("deposit_amount")


    if(len(accno_last4)==4):
        depo=deposit_withdraw(accno_last4,deposit_amount,0,CustomerId)
        result=depo.deposit()
        return (jsonify(result), 200) if result["success"] else (jsonify(result), 404)
    
    return jsonify({"success":False, "Error":" please enter only the last -4 digits- of the account number"}),400 



@app.route("/withdraw",methods=["POST"])
@jwt_required()
def Withdraw():
    claims=get_jwt()
    role=claims.get("role")
    CustomerId=claims.get("customer_id")

    if(role!="customer"):
        return jsonify({"success":False, "Error":"Access denied"}),403
    
    data=request.get_json()
    accno_last4=data.get("accno_last4")
    withdraw_amount=data.get("withdraw_amount")
    
    if(len(accno_last4)==4):
        withd=deposit_withdraw(accno_last4,0,withdraw_amount,CustomerId)
        result=withd.withdraw()
        return (jsonify(result), 200) if result["success"] else (jsonify(result), 404)
    
    return jsonify({"success":False, "Error":" please enter only the last -4 digits- of the account number"}),400 
    

@app.route("/transfer",methods=["POST"])
@jwt_required()
def Transfer():
    claims=get_jwt()
    role=claims.get("role")

    if(role!="customer"):
        return jsonify({"success":False, "Error":"Access denied"}),403
    
    data=request.get_json()
    sender=data.get("sender_accno_last4")
    receiver=data.get("receiver_accno_last4")
    amount=data.get("amount")
    
    if(len(sender)==4 and len(receiver)==4):
         trans=TransferAmounts(sender,receiver,amount)
         result=trans.transfer()
         return (jsonify(result), 200) if result["success"] else (jsonify(result), 404)
    return jsonify({"success":False, "Error":" please only  enter the last -4 digits- of the sender's and receiver's account number"}),400 



if (__name__ == "__main__"):
    with app.app_context():
        db.create_all()
    app.run()
