from django.urls import path
from Restaurants import views
app_name = "webRestaurants"
urlpatterns=[
        path('AddTable/',views.AddTable,name="AddTable"),
        path('AddWaiter/',views.AddWaiter,name="AddWaiter"),
        path('AddFood/',views.AddFood,name="AddFood"),
        path('AjaxCategory/',views.AjaxCategory,name="AjaxCategory"),
        path('AjaxPlace/',views.AjaxPlace,name="AjaxPlace"),
        path('Complains/',views.Complains,name="Complains"),
        path('MyProfile/',views.MyProfile,name="MyProfile"),
        path('EditProfile/',views.EditProfile,name="EditProfile"),
        path('ChangePassword/',views.ChangePassword,name="ChangePassword"),
        path('ViewBooking/',views.ViewBooking,name="ViewBooking"),
        path('ReassignWaiter/',views.ReassignWaiter,name="ReassignWaiter"),
        path('Homepage/',views.Homepage,name="Homepage"),
        path('Accepted/<str:id>',views.Accepted,name="Accepted"),
        path('Rejected/<str:id>',views.Rejected,name="Rejected"),

]