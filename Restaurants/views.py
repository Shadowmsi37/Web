from django.shortcuts import render,redirect
import firebase_admin
from firebase_admin import credentials,auth,firestore
import pyrebase
# Create your views here.


db = firestore.client()

def AddTable(request):
    return render(request,"Restaurants/AddTable.html")

def AddWaiter(request):
    return render(request,"Restaurants/AddWaiter.html")

def AddFood(request):
    return render(request,"Restaurants/AddFood.html")

def Complains(request):
    return render(request,"Restaurants/Complains.html")

def MyProfile(request):
    return render(request,"Restaurants/MyProfile.html")

def EditProfile(request):
    return render(request,"Restaurants/EditProfile.html")

def ChangePassword(request):
    return render(request,"Restaurants/ChangePassword.html")