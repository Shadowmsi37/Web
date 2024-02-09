from django.urls import path
from Admin import views
app_name = "webadmin"
urlpatterns=[
        path('district/',views.district,name="district"),
        path('Place/',views.Place,name="Place"),
        path('FoodType/',views.FoodType,name="FoodType"),
        path('Category/',views.Category,name="Category"),
        path('Admin/',views.Admin,name="Admin"),
        path('delAdmin/<str:id>',views.delAdmin,name="delAdmin"),
        path('editAdmin/<str:id>',views.editAdmin,name="editAdmin"),
        path('deldistrict/<str:id>',views.deldistrict,name="deldistrict"),
        path('editdistrict/<str:id>',views.editdistrict,name="editdistrict"),
        path('delPlace/<str:id>',views.delPlace,name="delPlace"),
        path('editPlace/<str:id>',views.editPlace,name="editPlace"),
        path('delFoodType/<str:id>',views.delFoodType,name="delFoodType"),
        path('delCategory/<str:id>',views.delCategory,name="delCategory")

]