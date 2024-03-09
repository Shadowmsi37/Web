from django.shortcuts import render,redirect
import firebase_admin
from firebase_admin import credentials,auth,firestore,storage
import pyrebase
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
        db.collection("tbl_Restaurant").add({"Restaurant_id":Restaurant.uid,"Restaurant_Name":request.POST.get("Name"),"Restaurant_Email":request.POST.get("Email"),"Restaurant_Contact":request.POST.get("Contact"),"Restaurant_Address":request.POST.get("Address"),"place_id":request.POST.get("place"),"Restaurant_Photo":rp_url,"Restaurant_Status":0})
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
        db.collection("tbl_Customer").add({"Customer_id":Customer.uid,"Customer_Name":request.POST.get("Name"),"Customer_Email":request.POST.get("Email"),"Customer_Contact":request.POST.get("Contact"),"Customer_Address":request.POST.get("Address"),"place_id":request.POST.get("place"),"Customer_Photo":cp_url})
        return render(request,"Guest/CustomerRegistration.html")
    else:    
        return render(request,"Guest/CustomerRegistration.html",{"district":dis_data})


def Login(request):
    Customerid = ""
    Restaurantid =""
    Adminid =""
    Waiterid=""
    if request.method == "POST":
        email = request.POST.get("Email")
        password = request.POST.get("Password")
        try:
            data = authe.sign_in_with_email_and_password(email,password)
        except:
            return render(request,"Guest/Login.html",{"msg":"Error in Email Or Password"})
        Customer=db.collection("tbl_Customer").where("Customer_id","==",data["localId"]).stream() 
        for c in Customer:
            Customerid=c.id
        Waiter=db.collection("tbl_Waiter").where("Waiter_id","==",data["localId"]).stream() 
        for w in Waiter:
            Waiterid=w.id
        Admin=db.collection("tbl_Admin").where("Admin_id","==",data["localId"]).stream() 
        for a in Admin:
            Adminid=a.id   
        Restaurant = db.collection("tbl_Restaurant").where("Restaurant_id", "==",data["localId"],).stream()
        for r in Restaurant:
            Restaurantid = r.id  
        if Customerid:
            request.session["cid"] = Customerid
            return redirect("webcustomer:Homepage")  
        elif Restaurantid:
            request.session["rid"]=Restaurantid    
            return redirect("webRestaurants:Homepage")
        elif Waiterid:
            request.session["wid"]=Waiterid    
            return redirect("webwaiter:Homepage")
        elif Adminid:
            request.session["aid"]=Adminid    
            return redirect("webadmin:Homepage")
        else:
            return render(request,"Guest/Login.html",{"msg":"error"})    
    else:
       return render(request,"Guest/Login.html")  

def ForgetPassword(request):
    if request.method == "POST":
        Email = request.POST.get("Email")
        Customer = db.collection("tbl_Customer").document(request.session["cid"]).get().to_dict()
        customer_email = Customer.get("Customer_Email")
        
        Restaurant = db.collection("tbl_Restaurant").document(request.session["rid"]).get().to_dict()
        restaurant_email = Restaurant.get("Restaurant_Email")
        
        Waiter = db.collection("tbl_Waiter").document(request.session["wid"]).get().to_dict()
        waiter_email = Waiter.get("Waiter_Email")
        
        if Email == customer_email:
            password_link = firebase_admin.auth.generate_password_reset_link(customer_email) 
            send_mail(
                'Reset your password ', 
                "\rHello \r\nFollow this link to reset your Project password for your " + customer_email + "\n" + password_link +".\n If you didn't ask to reset your password, you can ignore this email. \r\n Thanks. \r\n Your user.",#body
                settings.EMAIL_HOST_USER,
                [customer_email],
                )
            return render(request, "Guest/CustomerResetLinkSent.html")
        elif Email == restaurant_email:
            send_mail(
                'Reset your password ', 
                "\rHello \r\nFollow this link to reset your Project password for your " + restaurant_email + "\n" + password_link +".\n If you didn't ask to reset your password, you can ignore this email. \r\n Thanks. \r\n Your user.",#body
                settings.EMAIL_HOST_USER,
                [restaurant_email],
                )
            return render(request, "Guest/RestaurantResetLinkSent.html")
        elif Email == waiter_email:
            send_mail(
                'Reset your password ', 
                "\rHello \r\nFollow this link to reset your Project password for your " + waiter_email + "\n" + password_link +".\n If you didn't ask to reset your password, you can ignore this email. \r\n Thanks. \r\n Your user.",#body
                settings.EMAIL_HOST_USER,
                [waiter_email],
                )
            return render(request, "Guest/WaiterResetLinkSent.html")
        else:
            return render(request, "Guest/Login.html")
          
def index(request):
    return render(request,"Guest/index.html")
