from django.urls import path
from Waiter import views
app_name = "webwaiter"
urlpatterns=[
        path('MyProfile/',views.MyProfile,name="MyProfile"),
        path('EditProfile/',views.EditProfile,name="EditProfile"),
        path('ChangePassword/',views.ChangePassword,name="ChangePassword"),
        path('Homepage/',views.Homepage,name="Homepage"),


]