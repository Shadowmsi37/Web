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
    Waiter=db.collection("tbl_Waiter").document(request.session["wid"]).get().to_dict()
    return render(request,"Waiter/MyProfile.html",{"Waiter":Waiter})

def EditProfile(request):
    Waiter=db.collection("tbl_Waiter").document(request.session["wid"]).get().to_dict()
    if request.method=="POST":
        data={"Waiter_Name":request.POST.get("Name"),"Waiter_Email":request.POST.get("Email"),"Waiter_Contact":request.POST.get("Contact")}
        db.collection("tbl_Waiter").document(request.session["wid"]).update(data)
        return redirect("webwaiter:MyProfile")
    else:
        return render(request,"Waiter/EditProfile.html",{"Waiter":Waiter})


def ChangePassword(request):
    Waiter = db.collection("tbl_Waiter").document(request.session["wid"]).get().to_dict()
    email = Waiter["Waiter_Email"]
    password_link = firebase_admin.auth.generate_password_reset_link(email) 
    send_mail(
    'Reset your password ', 
    "\rHello \r\nFollow this link to reset your Project password for your " + email + "\n" + password_link +".\n If you didn't ask to reset your password, you can ignore this email. \r\n Thanks. \r\n Your D MARKET user.",#body
    settings.EMAIL_HOST_USER,
    [email],
    )
    return render(request,"Waiter/Homepage.html",{"msg":email})

def Homepage(request):
    return render(request,"Waiter/Homepage.html")