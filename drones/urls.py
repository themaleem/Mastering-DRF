from django.urls import path
from drones import views
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register("drone-categories2",views.DroneCategoryList2)

urlpatterns = [
    path('drone-categories/',views.DroneCategoryList.as_view(),name=views.DroneCategoryList.name),
    path('drone-categories/<int:pk>',views.DroneCategoryDetail.as_view(),name=views.DroneCategoryDetail.name),
    path('drones/',views.DroneList.as_view(),name=views.DroneList.name),
    path('drones/<int:pk>',views.DroneDetail.as_view(),name=views.DroneDetail.name),
    path('pilots/',views.PilotList.as_view(),name=views.PilotList.name),
    path('pilots/<int:pk>',views.PilotDetail.as_view(),name=views.PilotDetail.name),
    path('competitions/',views.CompetitionList.as_view(),name=views.CompetitionList.name),
    path('competitions/<int:pk>',views.CompetitionDetail.as_view(),name=views.CompetitionDetail.name),
    path('users/',views.UserList.as_view(),name=views.UserList.name),
    path('users/<int:pk>',views.UserDetail.as_view(),name=views.UserDetail.name),
    path('',views.ApiRoot.as_view(),name=views.ApiRoot.name),
]
urlpatterns+=router.urls