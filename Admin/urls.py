from django.urls import path
from Admin import views
app_name = "webadmin"
urlpatterns=[
        path('district/',views.district,name="district"),
        path('deldistrict/<str:id>',views.deldistrict,name="deldistrict"),
        path('editdistrict/<str:id>',views.editdistrict,name="editdistrict"),
        path('Place/',views.Place,name="Place"),
        path('delPlace/<str:id>',views.delPlace,name="delPlace"),
        path('editPlace/<str:id>',views.editPlace,name="editPlace"),
        path('Admin/',views.Admin,name="Admin"),          
        path('MyProfile/',views.MyProfile,name="MyProfile"),
        path('EditProfile/',views.EditProfile,name="EditProfile"),
        path('ChangePassword/',views.ChangePassword,name="ChangePassword"),
        path('ViewRestaurant/',views.ViewRestaurant,name="ViewRestaurant"),
        path('Accepted/<str:id>',views.Accepted,name="Accepted"),
        path('Rejected/<str:id>',views.Rejected,name="Rejected"),
        path('Homepage/',views.Homepage,name="Homepage"),
        path('ViewComplains/',views.ViewComplains,name="ViewComplains"),   

]