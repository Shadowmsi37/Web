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
            return render(request,"Restaurants/AddWaiter.html",{"msg":error})
      
        image=request.FILES.get("Photo")
        if image:
            path="WaiterPhoto/"+image.name
            st.child(path).put(image)
            wp_url=st.child(path).get_url(None)

        image=request.FILES.get("Photo")
        if image:
            path="WaiterProof/"+image.name
            st.child(path).put(image)
            wpr_url=st.child(path).get_url(None)
        db.collection("tbl_Waiter").add({"Waiter_id":Waiter.uid,"Waiter_Name":request.POST.get("Name"),"Waiter_Email":request.POST.get("Email"),"Waiter_Contact":request.POST.get("Contact"),"Waiter_Address":request.POST.get("Address"),"place_id":request.POST.get("place"),"Waiter_Proof":wpr_url,"Waiter_Photo":wp_url})
        return render(request,"Restaurants/AddWaiter.html")
    else:    
        return render(request,"Restaurants/AddWaiter.html",{"district":dis_data})

def AjaxPlace(request):
    place=db.collection("tbl_place").where("district_id","==",request.GET.get("did")).stream()
    place_data=[]
    for p in place:
        place_data.append({"place":p.to_dict(),"id":p.id})
    return render(request,"Restaurants/AjaxPlace.html",{"place":place_data})


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
    com=db.collection("tbl_Complains").stream()
    com_data=[]
    for i in com:
        data=i.to_dict()
        com_data.append({"com":data,"id":i.id})
    if request.method=="POST":
        data={"Complains_name":request.POST.get("Title"),"Complains_Content":request.POST.get("Content")}
        db.collection("tbl_Complains").add(data)
        return redirect("webRestaurants:Complains")
    else:
        return render(request,"Restaurants/Complains.html",{"Complains":com_data})



def MyProfile(request):
    return render(request,"Restaurants/MyProfile.html")

def EditProfile(request):
    return render(request,"Restaurants/EditProfile.html")

def ChangePassword(request):
    return render(request,"Restaurants/ChangePassword.html")

def Homepage(request):
    return render(request,"Restaurants/Homepage.html")