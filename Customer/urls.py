from django.urls import path
from Customer import views
app_name = "webcustomer"
urlpatterns=[
        path('MyProfile/',views.MyProfile,name="MyProfile"),
        path('EditProfile/',views.EditProfile,name="EditProfile"),
        path('ChangePassword/',views.ChangePassword,name="ChangePassword"),

]