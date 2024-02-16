from django.shortcuts import render,redirect
import firebase_admin
from firebase_admin import credentials,auth,firestore
import pyrebase
# Create your views here.



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


def delAdmin(request,id):
    db.collection("tbl_Admin").document(id).delete()
    return redirect("webadmin:Admin") 

def editAdmin(request,id):
    a=db.collection("tbl_Admin").document(id).get().to_dict()
    if request.method=="POST":
        data = {"Admin_Name":request.POST.get("Name"),"Admin_Email":request.POST.get("Email"),"Admin_Contact":request.POST.get("Contact")}
        db.collection("tbl_Admin").document(id).update(data)
        return redirect("webadmin:Admin")
    else:
        return render(request,"Admin/Admin.html",{"Admin_data":a}) 
    
def Homepage(request):
    return render(request,"Admin/Homepage.html") 

   
