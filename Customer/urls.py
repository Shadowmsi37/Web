from django.urls import path
from Customer import views
app_name = "webcustomer"
urlpatterns=[
        path('MyProfile/',views.MyProfile,name="MyProfile"),
        path('EditProfile/',views.EditProfile,name="EditProfile"),
        path('ChangePassword/',views.ChangePassword,name="ChangePassword"),
        path('Homepage/',views.Homepage,name="Homepage"),
        path('ViewTable/<str:id>',views.ViewTable,name="ViewTable"),
        path('ViewRestaurant/',views.ViewRestaurant,name="ViewRestaurant"),
        path('Booking/<str:id>',views.Booking,name="Booking"),
        path('Complains/',views.Complains,name="Complains"),
        path('Payment/',views.Payment,name="Payment"),
        path('loader/',views.loader,name="loader"),
        path('paymentsuc/',views.paymentsuc,name="paymentsuc"),
]