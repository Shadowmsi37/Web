from django.shortcuts import render,redirect
import firebase_admin
from firebase_admin import credentials,auth,firestore
import pyrebase

from Admin.views import FoodType
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

def AddTable(request):
    return render(request,"Restaurants/AddTable.html")

def AddWaiter(request):
    return render(request,"Restaurants/AddWaiter.html")

def AddFood(request):
    ft=db.collection("tbl_Category").stream()
    ft_data=[]
    for i in ft:
        data=i.to_dict()
        ft_data.append({"ft":data,"id":i.id})
    if request.method=="POST":
        
        image=request.FILES.get("Photo")
        if image:
            path="FoodPhoto/"+image.name
            st.child(path).put(image)
            fp_url=st.child(path).get_url(None)
        db.collection("tbl_Food").add({"Food_id":FoodType.uid,"Food_Name":request.POST.get("Name"),"Food_Price":request.POST.get("Price"),"Food_Description":request.POST.get("Description"),"FoodType_id":request.POST.get("FoodType"),"Food_Photo":fp_url})
        return render(request,"Restaurants/AddFood.html")
    else:    
        return render(request,"Restaurants/AddFood.html",{"Category":ft_data})

def AjaxCategory(request):
    Category=db.collection("tbl_Category").where("FoodType_id","==",request.GET.get("did")).stream()
    Category_data=[]
    for ft in Category:
        Category_data.append({"Category":ft.to_dict(),"id":ft.id})
    return render(request,"Restaurants/AjaxCategory.html",{"Category":Category_data})


def Complains(request):
    return render(request,"Restaurants/Complains.html")

def MyProfile(request):
    return render(request,"Restaurants/MyProfile.html")

def EditProfile(request):
    return render(request,"Restaurants/EditProfile.html")

def ChangePassword(request):
    return render(request,"Restaurants/ChangePassword.html")

def Homepage(request):
    return render(request,"Restaurants/Homepage.html")