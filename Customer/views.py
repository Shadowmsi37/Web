from django.shortcuts import render,redirect
import firebase_admin
from firebase_admin import credentials,auth,firestore
import pyrebase
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from datetime import date
# Create your views here.


db = firestore.client()

def MyProfile(request):
    if "cid" in request.session:
        Customer=db.collection("tbl_Customer").document(request.session["cid"]).get().to_dict()
        return render(request,"Customer/MyProfile.html",{"Customer":Customer})
    else:
        return render(request,"Guest/Login.html")
    
def EditProfile(request):
    Customer=db.collection("tbl_Customer").document(request.session["cid"]).get().to_dict()
    if request.method=="POST":
        data={"Customer_Name":request.POST.get("Name"),"Customer_Contact":request.POST.get("Contact")}
        db.collection("tbl_Customer").document(request.session["cid"]).update(data)
        return redirect("webcustomer:MyProfile")
    else:
        return render(request,"Customer/EditProfile.html",{"Customer":Customer})


def ChangePassword(request):
    Customer = db.collection("tbl_Customer").document(request.session["cid"]).get().to_dict()
    email = Customer["Customer_Email"]
    password_link = firebase_admin.auth.generate_password_reset_link(email) 
    send_mail(
    'Reset your password ', 
    "\rHello \r\nFollow this link to reset your Project password for your " + email + "\n" + password_link +".\n If you didn't ask to reset your password, you can ignore this email. \r\n Thanks. \r\n Your user.",#body
    settings.EMAIL_HOST_USER,
    [email],
    )
    return render(request,"Customer/Homepage.html",{"msg":email})

def ViewTable(request,id):
    if "cid" in request.session:
        t=db.collection("tbl_Table").where("Restaurant_id", "==", id).stream()
        t_data=[]
        for i in t:
            data=i.to_dict()
            t_data.append({"t":data,"id":i.id})
        return render(request,"Customer/ViewTable.html",{"Table":t_data})
    else:
        return render(request,"Guest/Login.html")
    
def Homepage(request):
    if "cid" in request.session:
        return render(request,"Customer/Homepage.html")
    else:
        return render(request,"Guest/Login.html")
    
def Payment(request):
    pay = db.collection("tbl_Booking").where("Booking_Status", "==",0).where("Customer_id", "==",request.session["cid"]).where("payment_status", "==",0).stream()
    ids = ""
    for i in pay:
        ids = i.id
    # print(ids)
    if request.method == "POST":
        db.collection("tbl_Booking").document(ids).update({"payment_status":1})
        return redirect("webcustomer:loader")
        # return render(request,"Customer/Payment.html")
    else:
        return render(request,"Customer/Payment.html")

def loader(request):
    return render(request,"Customer/Loader.html")

def paymentsuc(request):
    return render(request,"Customer/Payment_suc.html")

def ViewRestaurant(request):
    if "cid" in request.session:
        vr=db.collection("tbl_Restaurant").stream()
        vr_data=[]
        rate_len = 0
        for i in vr:
            data=i.to_dict()
            rating_count = db.collection("tbl_rating").where("shop_id", "==", i.id).stream()
            for rc in rating_count:
                rate_d = rc.to_dict()
                rate_len = rate_len + int(len(rate_d))
            r_len = rate_len//5
            res = 0
            avg = 0
            rating = db.collection("tbl_rating").where("shop_id", "==", i.id).stream()
            for r in rating:
                rate = r.to_dict()
                res = res + int(rate["rating_data"])
                avg = res//r_len 
            vr_data.append({"vr":data,"id":i.id,"avg":avg})
        return render(request,"Customer/ViewRestaurant.html",{"Restaurant":vr_data})
    else:
        return render(request,"Guest/Login.html")
    

def Booking(request,id):
    b=db.collection("tbl_Booking").where("Restaurant_id", "==", id).stream()
    b_data=[]
    for i in b:
        data=i.to_dict()
        b_data.append({"b":data,"id":i.id})
    if request.method=="POST":
        data={"Table_id":id,"Customer_id":request.session["cid"],"Date":request.POST.get("Date"),"Time":request.POST.get("Time"),"Booking_Status":0,"payment_status":0,"Waiter_Status":0,"Waiter_id":""}
        db.collection("tbl_Booking").add(data)
        return redirect("webcustomer:Payment")
    else:
        return render(request,"Customer/Booking.html")
    
def ViewBooking(request):
    return render(request,"Customer/Booking.html")

    

def Complains(request):
    if "cid" in request.session:
        com=db.collection("tbl_Complains").stream()
        com_data=[]
        for i in com:
            data=i.to_dict()
            com_data.append({"com":data,"id":i.id})
        if request.method=="POST":
            data={"Complains_Name":request.POST.get("Title"),"Complains_Content":request.POST.get("Content"),"Complains_Status":0,"Restaurant_id":"","waiter_id":"","Customer_id":request.session["cid"]}
            db.collection("tbl_Complains").add(data)
            return redirect("webcustomer:Complains")
        else:
            return render(request,"Restaurants/Complains.html",{"Complains":com_data})
    else:
        return render(request,"Guest/Login.html")
    
def rating(request,cid):
    parray=["1","2","3","4","5"]    
    # cdata = db.collection("tbl_cart").document(cid).get().to_dict()
    count = 0
    r_len = 0
    r_data = []
    rate = db.collection("tbl_rating").where("shop_id", "==", cid).stream()
    for i in rate:
        rdata = i.to_dict()
        r_len = r_len + int(len(rdata))
    rlen = r_len // 5
    if rlen>0:
        res=0    
        ratedata = db.collection("tbl_rating").where("shop_id", "==", cid).stream()
        for i in ratedata:
            rated = i.to_dict()
            r_data.append({"data":i.to_dict()})
            res = res + int(rated["rating_data"])
            avg = res//rlen
        return render(request,"Customer/Rating.html",{"cid":cid,"data":r_data,"ar":parray,"avg":avg,"count":rlen})
    else:
        return render(request,"Customer/Rating.html",{'cid':cid})

def ajaxrating(request):
    parray=[1,2,3,4,5]
    rate_data = []
    # cart = db.collection("tbl_cart").document(request.GET.get('workid')).get().to_dict()
    datedata = date.today()
    db.collection("tbl_rating").add({"rating_data":request.GET.get('rating_data'),"user_name":request.GET.get('user_name'),"user_review":request.GET.get('user_review'),"shop_id":request.GET.get("workid"),"date":str(datedata)})
    pdt = db.collection("tbl_rating").where("shop_id", "==", request.GET.get('workid')).stream()
    for p in pdt:
        rate_data.append({"rate":p.to_dict(),"id":p.id})
    return render(request,"Customer/AjaxRating.html",{'data':rate_data,'ar':parray})

def starrating(request):
    r_len = 0
    five = four = three = two = one = 0
    # cdata = db.collection("tbl_cart").document(request.GET.get("pdt")).get().to_dict()
    rate = db.collection("tbl_rating").where("shop_id", "==", request.GET.get('pdt')).stream()
    for i in rate:
        rated = i.to_dict()
        if int(rated["rating_data"]) == 5:
            five = five + 1
        elif int(rated["rating_data"]) == 4:
            four = four + 1
        elif int(rated["rating_data"]) == 3:
            three = three + 1
        elif int(rated["rating_data"]) == 2:
            two = two + 1
        elif int(rated["rating_data"]) == 1:
            one = one + 1
        else:
            five = four = three = two = one = 0
        r_len = r_len + int(len(rated))
    rlen = r_len // 5
    result = {"five":five,"four":four,"three":three,"two":two,"one":one,"total_review":rlen}
    return JsonResponse(result)

def Logout(request):
    del request.session["cid"]
    return redirect("webguest:Login")
