from django.shortcuts import render,redirect
import firebase_admin
from firebase_admin import credentials,auth,firestore
import pyrebase
# Create your views here.


db = firestore.client()

def MyProfile(request):
    return render(request,"Customer/MyProfile.html")

def EditProfile(request):
    return render(request,"Customer/EditProfile.html")

def ChangePassword(request):
    return render(request,"Customer/ChangePassword.html")

def Homepage(request):
    return render(request,"Customer/Homepage.html")