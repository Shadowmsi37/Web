from django.shortcuts import render,redirect
import firebase_admin
from firebase_admin import credentials,auth,firestore
import pyrebase
# Create your views here.


db = firestore.client()

def MyProfile(request):
    return render(request,"Waiter/MyProfile.html")

def EditProfile(request):
    return render(request,"Waiter/EditProfile.html")

def ChangePassword(request):
    return render(request,"Waiter/ChangePassword.html")