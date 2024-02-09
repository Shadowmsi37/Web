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
        path('delAdmin/<str:id>',views.delAdmin,name="delAdmin"),
        path('editAdmin/<str:id>',views.editAdmin,name="editAdmin"),
        path('FoodType/',views.FoodType,name="FoodType"),
        path('delFoodType/<str:id>',views.delFoodType,name="delFoodType"),
        path('editFoodType/<str:id>',views.editFoodType,name="editFoodType"),
        path('Category/',views.Category,name="Category"),
        path('delCategory/<str:id>',views.delCategory,name="delCategory"),
        path('editCategory/<str:id>',views.editCategory,name="editCategory")        

]