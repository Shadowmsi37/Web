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
        data={"Waiter_Name":request.POST.get("Name"),"Waiter_Contact":request.POST.get("Contact")}
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
    "\rHello \r\nFollow this link to reset your Project password for your " + email + "\n" + password_link +".\n If you didn't ask to reset your password, you can ignore this email. \r\n Thanks. \r\n Your user.",#body
    settings.EMAIL_HOST_USER,
    [email],
    )
    return render(request,"Waiter/Homepage.html",{"msg":email})


def ViewCustomers(request):
    vc = db.collection("tbl_Booking").where("Waiter_id","==",request.session["wid"]).stream()
    vc_data=[]
    for i in vc:
            data=i.to_dict()
            Customer=db.collection("tbl_Customer").document(data["Customer_id"]).get().to_dict()
            Booking=db.collection("tbl_Booking").document(data["Customer_id"]).get().to_dict()
            Table=db.collection("tbl_Table").document(data["Table_id"]).get().to_dict()
            vc_data.append({"view":data,"id":i.id,"Customer":Customer,"Booking":Booking,"Table":Table})
            return render(request,"Waiter/ViewCustomers.html",{"view":vc_data})
    else:
        return render(request,"Waiter/ViewCustomers.html")
    
def Accepted(request,id):
    req=db.collection("tbl_Booking").where("Waiter_id", "==", request.session["wid"]).stream()
    w=db.collection("tbl_Waiter").where("Restaurant_id", "==", request.session["rid"]).stream()
    w_data=[]
    for i in w:
        data=i.to_dict()
        w_data.append({"w":data,"id":i.id})
        data={"Waiter_id":request.session["wid"],"Waiter_Status":1}
        db.collection("tbl_Booking").document(id).update(data)
        return render(request,"Waiter/Homepage.html")   
    else:
         return render(request,"Waiter/Homepage.html",{"Waiter":w_data})
    


def Rejected(request,id):
    req=db.collection("tbl_Booking").document(id).update({"Waiter_id":"","Booking_Status":0})
    bk = db.collection("tbl_Booking").document(id).get().to_dict()
    Customer = db.collection("tbl_Customer").document(bk["Customer_id"]).get().to_dict()
    email = Customer["Customer_Email"]
    send_mail(
    'Reservation Status', 
    "\rHello \r\n Our Waiter is not feel good today \r\n we will assign another waiter shortly",#body
    settings.EMAIL_HOST_USER,
    [email],
    )
    return render(request,"Waiter/Homepage.html",{"msg":email}) 



def Homepage(request):
    return render(request,"Waiter/Homepage.html")