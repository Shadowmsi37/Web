from django.shortcuts import render,redirect
import firebase_admin
from firebase_admin import credentials,auth,firestore,storage
import pyrebase
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


def AjaxPlace(request):
    place=db.collection("tbl_place").where("district_id","==",request.GET.get("did")).stream()
    place_data=[]
    for p in place:
        place_data.append({"place":p.to_dict(),"id":p.id})
    return render(request,"Guest/AjaxPlace.html",{"place":place_data})

def AjaxCategory(request):
    Category=db.collection("tbl_Category").where("FoodType_id","==",request.GET.get("did")).stream()
    Category_data=[]
    for ft in Category:
        Category_data.append({"Category":ft.to_dict(),"id":ft.id})
    return render(request,"Guest/AjaxCategory.html",{"Category":Category_data})


def RestaurantRegistration(request):
    dis=db.collection("tbl_district").stream()
    dis_data=[]
    for i in dis:
        data=i.to_dict()
        dis_data.append({"dis":data,"id":i.id})
    if request.method=="POST":
        email = request.POST.get("Email")
        password = request.POST.get("Password")
        try:
            Restaurant = firebase_admin.auth.create_user(email=email,password=password)
        except (firebase_admin._auth_utils.EmailAlreadyExistsError,ValueError) as error:
            return render(request,"Guest/RestaurantRegistration.html",{"msg":error})
      
        image=request.FILES.get("Photo")
        if image:
            path="RestaurantPhoto/"+image.name
            st.child(path).put(image)
            rp_url=st.child(path).get_url(None)
        db.collection("tbl_Restaurant").add({"Restaurant_Name":request.POST.get("Name"),"Restaurant_Email":request.POST.get("Email"),"Restaurant_Contact":request.POST.get("Contact"),"Restaurant_Address":request.POST.get("Address"),"place_id":request.POST.get("place"),"Restaurant_Photo":rp_url})
        return render(request,"Guest/RestaurantRegistration.html")
    else:    
        return render(request,"Guest/RestaurantRegistration.html",{"district":dis_data})

def CustomerRegistration(request):
    dis=db.collection("tbl_district").stream()
    dis_data=[]
    for i in dis:
        data=i.to_dict()
        dis_data.append({"dis":data,"id":i.id})
    if request.method=="POST":
        email = request.POST.get("Email")
        password = request.POST.get("Password")
        try:
            Customer = firebase_admin.auth.create_user(email=email,password=password)
        except (firebase_admin._auth_utils.EmailAlreadyExistsError,ValueError) as error:
            return render(request,"Guest/CustomerRegistration.html",{"msg":error})
      
        image=request.FILES.get("Photo")
        if image:
            path="CustomerPhoto/"+image.name
            st.child(path).put(image)
            cp_url=st.child(path).get_url(None)
        db.collection("tbl_Customer").add({"Customer_Name":request.POST.get("Name"),"Customer_Email":request.POST.get("Email"),"Customer_Contact":request.POST.get("Contact"),"Customer_Address":request.POST.get("Address"),"place_id":request.POST.get("place"),"Customer_Photo":cp_url})
        return render(request,"Guest/CustomerRegistration.html")
    else:    
        return render(request,"Guest/CustomerRegistration.html",{"district":dis_data})


def Login(request):
    return render(request,"Guest/Login.html")