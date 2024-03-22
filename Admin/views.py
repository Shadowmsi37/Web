from django.shortcuts import render,redirect
import firebase_admin
from firebase_admin import credentials,auth,firestore
import pyrebase
# Create your views here.
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

# Create your views here.

db = firestore.client()
config = {
  "apiKey": "AIzaSyBeghB8L8iPzsMj-5tOttlQ0kdRDl4KmG0",
  "authDomain": "restaurants-reservation-system.firebaseapp.com",
  "projectId": "restaurants-reservation-system",
  "storageBucket": "restaurants-reservation-system.appspot.com",
  "messagingSenderId": "850141705565",
  "appId": "1:850141705565:web:c13260719ae357ecc4e4b4",
  "measurementId": "G-WXY3E1NQTX",
  "databaseURL":""
}

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
st = firebase.storage()
db = firestore.client()


def district(request):
    dis=db.collection("tbl_district").stream()
    dis_data=[]
    for i in dis:
        data=i.to_dict()
        dis_data.append({"dis":data,"id":i.id})
    if request.method=="POST":
        data={"district_name":request.POST.get("District")}
        db.collection("tbl_district").add(data)
        return redirect("webadmin:district")
    else:
        return render(request,"Admin/District.html",{"district":dis_data})
    
def deldistrict(request,id):
    db.collection("tbl_district").document(id).delete()
    return redirect("webadmin:district")   

def editdistrict(request,id):
    dis=db.collection("tbl_district").document(id).get().to_dict()
    if request.method=="POST":
        data={"district_name":request.POST.get("District")}
        db.collection("tbl_district").document(id).update(data)
        return redirect("webadmin:district")
    else:
        return render(request,"Admin/District.html",{"dis_data":dis}) 
   
def Place(request):
    dis=db.collection("tbl_district").stream()
    dis_data=[]
    for i in dis:
        data=i.to_dict()
        dis_data.append({"dis":data,"id":i.id})
    result=[]
    place_data=db.collection("tbl_place").stream()
    for place in place_data:
        place_dict=place.to_dict()
        district=db.collection("tbl_district").document(place_dict["district_id"]).get()
        district_dict=district.to_dict()
        result.append({'district_data':district_dict,'place_data':place_dict,'placeid':place.id})
    if request.method=="POST":
        data={"place_name":request.POST.get("Place"),"district_id":request.POST.get("district")}
        db.collection("tbl_place").add(data)
        return redirect("webadmin:Place")
    else:
        return render(request,"Admin/Place.html",{"district":dis_data,"place":result})
    
def delPlace(request,id):
    db.collection("tbl_place").document(id).delete()
    return redirect("webadmin:Place") 

def editPlace(request,id):
    db.collection()


def Admin(request):
    
    if request.method=="POST":
        email = request.POST.get("Email")
        password = request.POST.get("Password")
        try:
            Admin = firebase_admin.auth.create_user(email=email,password=password)
        except (firebase_admin._auth_utils.EmailAlreadyExistsError,ValueError) as error:
            return render(request,"Admin/Admin.html",{"msg":error})
      
        db.collection("tbl_Admin").add({"Admin_id":Admin.uid,"Admin_Name":request.POST.get("Name"),"Admin_Email":request.POST.get("Email"),"Admin_Contact":request.POST.get("Contact")})
        return render(request,"Admin/Admin.html")
    else:    
        return render(request,"Admin/Admin.html")
    
def MyProfile(request):
    Admin=db.collection("tbl_Admin").document(request.session["aid"]).get().to_dict()
    return render(request,"Admin/MyProfile.html",{"Admin":Admin})

def EditProfile(request):
    Admin=db.collection("tbl_Admin").document(request.session["aid"]).get().to_dict()
    if request.method=="POST":
        data={"Admin_Name":request.POST.get("Name"),"Admin_Contact":request.POST.get("Contact")}
        db.collection("tbl_Admin").document(request.session["aid"]).update(data)
        return redirect("webadmin:MyProfile")
    else:
        return render(request,"Admin/EditProfile.html",{"Admin":Admin})


def ChangePassword(request):
    Admin = db.collection("tbl_Admin").document(request.session["aid"]).get().to_dict()
    email = Admin["Admin_Email"]
    password_link = firebase_admin.auth.generate_password_reset_link(email) 
    send_mail(
    'Reset your password ', 
    "\rHello \r\nFollow this link to reset your Project password for your " + email + "\n" + password_link +".\n If you didn't ask to reset your password, you can ignore this email. \r\n Thanks. \r\n Your  user.",#body
    settings.EMAIL_HOST_USER,
    [email],
    )
    return render(request,"Admin/Homepage.html",{"msg":email})

    
def ViewRestaurant(request):
        vr = db.collection("tbl_Restaurant").where("Restaurant_Status","==",0).stream() 
        vr_data=[]
        for i in vr:
            data=i.to_dict()
            Restaurant=db.collection("tbl_Restaurant").document(data["Restaurant_id"]).get().to_dict()
            vr_data.append({"view":data,"id":i.id,"Restaurant":Restaurant})
            return render(request,"Admin/ViewRestaurant.html",{"view":vr_data})
        else:
            return render(request,"Admin/ViewRestaurant.html")

def Accepted(request,id):
    req=db.collection("tbl_Restaurant").document(id).update({"Restaurant_Status":1})
    # Restaurant = db.collection("tbl_Restaurant").document(request.session["rid"]).get().to_dict()
    # email = Restaurant["Restaurant_Email"]
    # send_mail(
    # 'Reservation Status', 
    # "\rHello \r\n Your Restaurant has  been Approved\r\n try to contact us",#body
    # settings.EMAIL_HOST_USER,
    # [email],
    # )
    return render(request,"Admin/ViewRestaurant.html",{"msg":email})
    


def Rejected(request,id):
    req=db.collection("tbl_Restaurant").document(id).update({"Restaurant_Status":2})
    # Restaurant = db.collection("tbl_Restaurant").document(request.session["rid"]).get().to_dict()
    # email = Restaurant["Restaurant_Email"]
    # send_mail(
    # 'Reservation Status', 
    # "\rHello \r\n Your Restaurant has not been Approved\r\n try to contact us",#body
    # settings.EMAIL_HOST_USER,
    # [email],
    # )
    return render(request,"Admin/ViewRestaurant.html",{"msg":email})


def ViewComplains(request):
    
        restaurant_data=[]
        customer_data=[]
        waiter_data=[]
        rcom = db.collection("tbl_Complains").where("Restaurant_id", "!=","").where("Complains_Status", "==", 0).stream()
        for i in rcom:
            rdata = i.to_dict()
            # print(rdata)
            restaurant = db.collection("tbl_Restaurant").document(rdata["Restaurant_id"]).get().to_dict()
            restaurant_data.append({"complaint":i.to_dict(),"id":i.id,"restaurant":restaurant})

        ccom=db.collection("tbl_Complains").where("Customer_id","!=","").where("Complains_Status","==",0).stream()
        for i in ccom:
            cdata = i.to_dict()
            customer = db.collection("tbl_Customer").document(cdata["Customer_id"]).get().to_dict()
            customer_data.append({"complaint":i.to_dict(),"id":i.id,"customer":customer}) 
        print(customer_data)

        wcom=db.collection("tbl_Complains").where("waiter_id","!=","").where("Complains_Status","==",0).stream()
        for i in wcom:
            wdata = i.to_dict()
            waiter = db.collection("tbl_Waiter").document(wdata["waiter_id"]).get().to_dict()
            waiter_data.append({"complaint":i.to_dict(),"id":i.id,"waiter":waiter})
            
        return render(request,"Admin/ViewComplains.html",{"restaurant":restaurant_data,"customer":customer_data,"waiter":waiter_data})    
    

    
def Homepage(request):
    return render(request,"Admin/Homepage.html")


   
