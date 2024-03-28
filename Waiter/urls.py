from django.urls import path
from Waiter import views
app_name = "webwaiter"
urlpatterns=[
        path('MyProfile/',views.MyProfile,name="MyProfile"),
        path('EditProfile/',views.EditProfile,name="EditProfile"),
        path('ChangePassword/',views.ChangePassword,name="ChangePassword"),
        path('Homepage/',views.Homepage,name="Homepage"),
        path('ViewCustomers/',views.ViewCustomers,name="ViewCustomers"),
        path('Accepted/<str:id>',views.Accepted,name="Accepted"),
        path('Rejected/<str:id>',views.Rejected,name="Rejected"),
        path('Complains/',views.Complains,name="Complains"),
        path('Logout/',views.Logout,name="Logout"),      


]