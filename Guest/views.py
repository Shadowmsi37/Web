from django.shortcuts import render,redirect
import firebase_admin
from firebase_admin import credentials,auth,firestore
import pyrebase
# Create your views here.


db = firestore.client()

def RestaurantRegistration(request):
    return render(request,"Guest/RestaurantRegistration.html")

def CustomerRegistration(request):
    return render(request,"Guest/CustomerRegistration.html")
   
def Complains(request):
    return render(request,"Guest/Complains.html")

def Login(request):
    return render(request,"Guest/Login.html")