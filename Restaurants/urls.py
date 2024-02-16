from django.urls import path
from Restaurants import views
app_name = "webRestaurants"
urlpatterns=[
        path('AddTable/',views.AddTable,name="AddTable"),
        path('AddWaiter/',views.AddWaiter,name="AddWaiter"),
        path('AddFood/',views.AddFood,name="AddFood"),
        path('AjaxCategory/',views.AjaxCategory,name="AjaxCategory"),
        path('Complains/',views.Complains,name="Complains"),
        path('MyProfile/',views.MyProfile,name="MyProfile"),
        path('EditProfile/',views.EditProfile,name="EditProfile"),
        path('ChangePassword/',views.ChangePassword,name="ChangePassword"),
        path('Homepage/',views.Homepage,name="Homepage"),


]