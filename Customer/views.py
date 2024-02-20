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
        data={"Customer_Name":request.POST.get("Name"),"Customer_Email":request.POST.get("Email"),"Customer_Contact":request.POST.get("Contact")}
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
    "\rHello \r\nFollow this link to reset your Project password for your " + email + "\n" + password_link +".\n If you didn't ask to reset your password, you can ignore this email. \r\n Thanks. \r\n Your D MARKET user.",#body
    settings.EMAIL_HOST_USER,
    [email],
    )
    return render(request,"Customer/Homepage.html",{"msg":email})

def Homepage(request):
    return render(request,"Customer/Homepage.html")