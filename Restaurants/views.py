from django.shortcuts import render,redirect
import firebase_admin
from firebase_admin import credentials,auth,firestore
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
db = firestore.client()

def AddTable(request):
    if "rid" in request.session:    
        if request.method=="POST":
            image=request.FILES.get("TablePhoto")
            if image:
                path="TablePhoto/"+image.name
                st.child(path).put(image)
                tp_url=st.child(path).get_url(None)
            db.collection("tbl_Table").add({"Restaurant_id":request.session["rid"],"Table_No":request.POST.get("Table_No"),"Table_Capacity":request.POST.get("Table_Capacity"),"Table_Photo":tp_url})
            return render(request,"Restaurants/Homeppage.html")
        else:    
            return render(request,"Restaurants/AddTable.html")
    else:
        return render(request,"Guest/Login.html")


def AddWaiter(request):
    if "rid" in request.session:
        dis=db.collection("tbl_district").stream()
        dis_data=[]
        for i in dis:
            data=i.to_dict()
            dis_data.append({"dis":data,"id":i.id})
        if request.method=="POST":
            email = request.POST.get("Email")
            password = request.POST.get("Password")
            try:
                Waiter = firebase_admin.auth.create_user(email=email,password=password)
            except (firebase_admin._auth_utils.EmailAlreadyExistsError,ValueError) as error:
                return render(request,"Restaurants/AddWaiter.html",{"msg":error})
        
            image=request.FILES.get("Photo")
            if image:
                path="WaiterPhoto/"+image.name
                st.child(path).put(image)
                wp_url=st.child(path).get_url(None)

            Proof=request.FILES.get("Proof")
            if image:
                path="WaiterProof/"+image.name
                st.child(path).put(image)
                wpr_url=st.child(path).get_url(None)
            db.collection("tbl_Waiter").add({"Restaurant_id":request.session["rid"],"Waiter_id":Waiter.uid,"Waiter_Name":request.POST.get("Name"),"Waiter_Email":request.POST.get("Email"),"Waiter_Contact":request.POST.get("Contact"),"Waiter_Address":request.POST.get("Address"),"place_id":request.POST.get("place"),"Waiter_Proof":wpr_url,"Waiter_Photo":wp_url})
            return render(request,"Restaurants/Homepage.html")
        else:    
            return render(request,"Restaurants/AddWaiter.html",{"district":dis_data})
    else:
        return render(request,"Guest/Login.html")
    
    
def AjaxPlace(request):
    if "rid" in request.session:
        place=db.collection("tbl_place").where("district_id","==",request.GET.get("did")).stream()
        place_data=[]
        for p in place:
            place_data.append({"place":p.to_dict(),"id":p.id})
        return render(request,"Restaurants/AjaxPlace.html",{"place":place_data})

def Complains(request):
    if "rid" in request.session:
        com=db.collection("tbl_Complains").stream()
        com_data=[]
        for i in com:
            data=i.to_dict()
            com_data.append({"com":data,"id":i.id})
        if request.method=="POST":
            data={"Complains_Name":request.POST.get("Title"),"Complains_Content":request.POST.get("Content"),"Complains_Status":0,"Restaurant_id":request.session["rid"],"waiter_id":"","customer_id":""}
            db.collection("tbl_Complains").add(data)
            return redirect("webRestaurants:Complains")
        else:
            return render(request,"Restaurants/Complains.html",{"Complains":com_data})
    else:
        return render(request,"Guest/Login.html")
    

def ViewComplains(request): 
        if "rid" in request.session:
            Table=db.collection("tbl_Table").where("Restaurant_id", "==", request.session["rid"]).stream()
            VC_data=[]
            for t in Table:
                VC = db.collection("tbl_Booking").where("Table_id","==",t.id).stream() 
                for i in VC:
                    data=i.to_dict()
                    Customer=db.collection("tbl_Customer").document(data["Customer_id"]).get().to_dict()
                    Table=db.collection("tbl_Table").document(data["Table_id"]).get().to_dict()
                    Complains=db.collection("tbl_Complains").document(data["Complains_id"]).get().to_dict()
                    VC_data.append({"view":data,"id":i.id,"Customer":Customer,"Table":Table,"Complains":Complains})
                    return render(request,"Restaurants/ViewComplains.html",{"view":VC_data})
        else:
            return render(request,"Guest/Login.html")



def MyProfile(request):
    if "rid" in request.session:
        Restaurant=db.collection("tbl_Restaurant").document(request.session["rid"]).get().to_dict()
        return render(request,"Restaurants/MyProfile.html",{"Restaurant":Restaurant})
    else:
        return render(request,"Guest/Login.html")
    

def EditProfile(request):
    Restaurant=db.collection("tbl_Restaurant").document(request.session["rid"]).get().to_dict()
    if request.method=="POST":
        data={"Restaurant_Name":request.POST.get("Name"),"Restaurant_Contact":request.POST.get("Contact"),"Restaurant_Address":request.POST.get("Address")}
        db.collection("tbl_Restaurant").document(request.session["rid"]).update(data)
        return redirect("webRestaurants:MyProfile")
    else:
        return render(request,"Restaurants/EditProfile.html",{"Restaurant":Restaurant})


def ChangePassword(request):
    Restaurant = db.collection("tbl_Restaurant").document(request.session["rid"]).get().to_dict()
    email = Restaurant["Restaurant_Email"]
    password_link = firebase_admin.auth.generate_password_reset_link(email) 
    send_mail(
    'Reset your password ', 
    "\rHello \r\nFollow this link to reset your Project password for your " + email + "\n" + password_link +".\n If you didn't ask to reset your password, you can ignore this email. \r\n Thanks. \r\n Your user.",#body
    settings.EMAIL_HOST_USER,
    [email],
    )
    return render(request,"Restaurants/Homepage.html",{"msg":email})

def ViewBooking(request):
        if "rid" in request.session:
            Table=db.collection("tbl_Table").where("Restaurant_id", "==", request.session["rid"]).stream()
            vb_data=[]
            for t in Table:
                vb = db.collection("tbl_Booking").where("Booking_Status","==",0).where("Table_id","==",t.id).stream() 
                for i in vb:
                    data=i.to_dict()
                    Customer=db.collection("tbl_Customer").document(data["Customer_id"]).get().to_dict()
                    Table=db.collection("tbl_Table").document(data["Table_id"]).get().to_dict()
                    vb_data.append({"view":data,"id":i.id,"Customer":Customer,"Table":Table})
                    return render(request,"Restaurants/ViewBooking.html",{"view":vb_data})


def Accepted(request,id):
    req=db.collection("tbl_Booking").stream()
    w=db.collection("tbl_Waiter").where("Restaurant_id", "==", request.session["rid"]).stream()
    w_data=[]
    for i in w:
        data=i.to_dict()
        w_data.append({"w":data,"id":i.id})
    if request.method=="POST":
        waiterdata = db.collection("tbl_Waiter").document(request.POST.get("Waiter")).get().to_dict()
        waiter_name = waiterdata["Waiter_Name"]
        data={"Waiter_id":request.POST.get("Waiter"),"Booking_Status":1}
        db.collection("tbl_Booking").document(id).update(data)
      
        Customer = db.collection("tbl_Customer").document(request.session["cid"]).get().to_dict()
        email = Customer["Customer_Email"]
        send_mail(
        'Reservation Status', 
        "\rHello \r\n Your Table has been Booked Successfully \r\n Your Waiter is " + waiter_name,#body
        settings.EMAIL_HOST_USER,
        [email],
        )
        
        return render(request,"Restaurants/Homepage.html",{"msg":email})   
    else:
         return render(request,"Restaurants/AssignWaiter.html",{"Waiter":w_data})
    


def Rejected(request,id):
    req=db.collection("tbl_Booking").document(id).update({"Booking_Status":2})
    Customer = db.collection("tbl_Customer").document(request.session["cid"]).get().to_dict()
    email = Customer["Customer_Email"]
    send_mail(
    'Reservation Status', 
    "\rHello \r\n Your Table Booking has been Rejected By Our Restaurant",#body
    settings.EMAIL_HOST_USER,
    [email],
    )
    return render(request,"Restaurants/ViewBooking.html",{"msg":email})    



def Homepage(request):
    if "rid" in request.session:
        return render(request,"Restaurants/Homepage.html")
    else:
        return render(request,"Guest/Login.html")
    
    
def Logout(request):
    del request.session["rid"]
    return redirect("webguest:Login")        