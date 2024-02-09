from django.urls import path
from Guest import views
app_name = "webguest"
urlpatterns=[
        path('RestaurantRegistration/',views.RestaurantRegistration,name="RestaurantRegistration"),
        path('CustomerRegistration/',views.CustomerRegistration,name="CustomerRegistration"),
        path('AjaxPlace/',views.AjaxPlace,name="AjaxPlace"),
        path('Login/',views.Login,name="Login"),

]