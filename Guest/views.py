from django.shortcuts import render,redirect
import firebase_admin
from firebase_admin import credentials,auth,firestore
import pyrebase
# Create your views here.


db = firestore.client()

def AjaxPlace(request):
    place=db.collection("tbl_place").where("district_id","==",request.GET.get("did")).stream()
    place_data=[]
    for p in place:
        place_data.append({"place":p.to_dict(),"id":p.id})
    return render(request,"Guest/AjaxPlace.html",{"place":place_data})


def RestaurantRegistration(request):
    return render(request,"Guest/RestaurantRegistration.html")

def CustomerRegistration(request):
    return render(request,"Guest/CustomerRegistration.html")
   
def Complains(request):
    return render(request,"Guest/Complains.html")

def Login(request):
    return render(request,"Guest/Login.html")