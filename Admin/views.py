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

   
def Category(request):

   ft = db.collection("tbl_Category").stream()
   ft_data = []
   for i in ft:
      ft_data.append({"Category":i.to_dict(),"id":i.id})
   if request.method == "POST":
      data = {"Category_name":request.POST.get("Category")}
      db.collection("tbl_Category").add(data)
      return redirect("webadmin:Category")
   else:
      return render(request,"Admin/Category.html",{"Category":ft_data})
   
def delCategory(request,id):
    db.collection("tbl_Category").document(id).delete()
    return redirect("webadmin:Category")

def editCategory(request,id):
    cat = db.collection("tbl_Category").document(id).get().to_dict()
    if request.method == "POST":
        db.collection("tbl_Category").document(id).update({"Category_name":request.POST.get("Category")})
        return redirect("webadmin:Category")
    else:
        return render(request,"Admin/Category.html",{"cat":cat})

      
def FoodType(request):
    ft=db.collection("tbl_Category").stream()
    ft_data=[]
    for i in ft:
        data=i.to_dict()
        ft_data.append({"ft":data,"id":i.id})
    result=[]
    FoodType_data=db.collection("tbl_FoodType").stream()
    for FoodType in FoodType_data:
        FoodType_dict=FoodType.to_dict()
        Category=db.collection("tbl_Category").document(FoodType_dict["Category_id"]).get().to_dict()
        result.append({'FoodType_data':FoodType_dict,'Category_data':Category,'FoodTypeid':FoodType.id})
    if request.method=="POST":
        data={"Category_id":request.POST.get("Category"),"FoodType_name":request.POST.get("FoodType")}
        db.collection("tbl_FoodType").add(data)
        return redirect("webadmin:FoodType")
    else:
        return render(request,"Admin/FoodType.html",{"Category":ft_data,"FoodType":result})
    
def delFoodType(request,id):
    db.collection("tbl_FoodType").document(id).delete()
    return redirect("webadmin:FoodType") 

def editFoodType(request,id):
    ft=db.collection("tbl_FoodType").document(id).get().to_dict()
    if request.method=="POST":
        data={"FoodType_name":request.POST.get("FoodType")}
        db.collection("tbl_FoodType").document(id).update(data)
        return redirect("webadmin:FoodType")
    else:
        return render(request,"Admin/FoodType.html",{"ft_data":ft})

         

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
        data={"Admin_Name":request.POST.get("Name"),"Admin_Email":request.POST.get("Email"),"Admin_Contact":request.POST.get("Contact")}
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
    req=db.collection("tbl_Restaurant").document(id).update({"Booking_Status":1})
    Restaurant = db.collection("tbl_Restaurant").document(request.session["rid"]).get().to_dict()
    email = Restaurant["Restaurant_Email"]
    send_mail(
    'Reservation Status', 
    "\rHello \r\n Your Restaurant has not been Approved\r\n try to contact us",#body
    settings.EMAIL_HOST_USER,
    [email],
    )
    return render(request,"Admin/ViewRestaurant.html",{"msg":email})
    


def Rejected(request,id):
    req=db.collection("tbl_Restaurant").document(id).update({"Booking_Status":2})
    Restaurant = db.collection("tbl_Restaurant").document(request.session["rid"]).get().to_dict()
    email = Restaurant["Restaurant_Email"]
    send_mail(
    'Reservation Status', 
    "\rHello \r\n Your Restaurant has not been Approved\r\n try to contact us",#body
    settings.EMAIL_HOST_USER,
    [email],
    )
    return render(request,"Admin/ViewRestaurant.html",{"msg":email})

    
def Homepage(request):
    return render(request,"Admin/Homepage.html") 

   
