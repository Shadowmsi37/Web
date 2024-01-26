from django.urls import path
from Admin import views
app_name = "webadmin"
urlpatterns=[
        path('District/',views.District,name="district"),
        path('Place/',views.Place,name="Place"),
        path('FoodType/',views.FoodType,name="FoodType"),
        path('Category/',views.Category,name="Category"),
         path('Admin/',views.Admin,name="Admin"),

]