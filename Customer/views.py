from django.shortcuts import render,redirect
import firebase_admin
from firebase_admin import credentials,auth,firestore
import pyrebase
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
# Create your views here.


db = firestore.client()

def MyProfile(request):
    Customer=db.collection("tbl_Customer").document(request.session["cid"]).get().to_dict()
    return render(request,"Customer/MyProfile.html",{"Customer":Customer})

def EditProfile(request):
    Customer=db.collection("tbl_Customer").document(request.session["cid"]).get().to_dict()
    if request.method=="POST":
        data={"Customer_Name":request.POST.get("Name"),"Customer_Contact":request.POST.get("Contact")}
        db.collection("tbl_Customer").document(request.session["cid"]).update(data)
        return redirect("webcustomer:MyProfile")
    else:
        return render(request,"Customer/EditProfile.html",{"Customer":Customer})


def ChangePassword(request):
    Customer = db.collection("tbl_Customer").document(request.session["cid"]).get().to_dict()
    email = Customer["Customer_Email"]
    password_link = firebase_admin.auth.generate_password_reset_link(email) 
    send_mail(
    'Reset your password ', 
    "\rHello \r\nFollow this link to reset your Project password for your " + email + "\n" + password_link +".\n If you didn't ask to reset your password, you can ignore this email. \r\n Thanks. \r\n Your user.",#body
    settings.EMAIL_HOST_USER,
    [email],
    )
    return render(request,"Customer/Homepage.html",{"msg":email})

def ViewTable(request,id):
    t=db.collection("tbl_Table").where("Restaurant_id", "==", id).stream()
    t_data=[]
    for i in t:
        data=i.to_dict()
        t_data.append({"t":data,"id":i.id})
    return render(request,"Customer/ViewTable.html",{"Table":t_data})

def Homepage(request):
    return render(request,"Customer/Homepage.html")

def Payment(request):
    pay = db.collection("tbl_Booking").where("Booking_Status", "==",0).where("Customer_id", "==",request.session["cid"]).where("payment_status", "==",0).stream()
    ids = ""
    for i in pay:
        ids = i.id
    # print(ids)
    if request.method == "POST":
        db.collection("tbl_Booking").document(ids).update({"payment_status":1})
        return redirect("webcustomer:loader")
        # return render(request,"Customer/Payment.html")
    else:
        return render(request,"Customer/Payment.html")

def loader(request):
    return render(request,"Customer/Loader.html")

def paymentsuc(request):
    return render(request,"Customer/Payment_suc.html")

def ViewRestaurant(request):
    vr=db.collection("tbl_Restaurant").stream()
    vr_data=[]
    for i in vr:
        data=i.to_dict()
        vr_data.append({"vr":data,"id":i.id})
    return render(request,"Customer/ViewRestaurant.html",{"Restaurant":vr_data})


def Booking(request,id):
    b=db.collection("tbl_Booking").where("Restaurant_id", "==", id).stream()
    b_data=[]
    for i in b:
        data=i.to_dict()
        b_data.append({"b":data,"id":i.id})
    if request.method=="POST":
        data={"Table_id":id,"Customer_id":request.session["cid"],"Date":request.POST.get("Date"),"Time":request.POST.get("Time"),"Booking_Status":0,"payment_status":0,"Waiter_Status":0,"Waiter_id":""}
        db.collection("tbl_Booking").add(data)
        return redirect("webcustomer:Payment")
    else:
        return render(request,"Customer/Booking.html")
    

def Complains(request):
    com=db.collection("tbl_Complains").stream()
    com_data=[]
    for i in com:
        data=i.to_dict()
        com_data.append({"com":data,"id":i.id})
    if request.method=="POST":
        data={"Complains_Name":request.POST.get("Title"),"Complains_Content":request.POST.get("Content"),"Complains_Status":0,"Reply":"","Customer_id":["cid"],"Restaurant_id":["rid"]}
        db.collection("tbl_Complains").add(data)
        return redirect("webcustomer:Complains")
    else:
        return render(request,"Customer/Complains.html",{"Complains":com_data})

