from django.urls import path
from . import views
urlpatterns=[
    path("",views.home,name="home"),
    path("room/<str:pk>/",views.room,name="room"),
    path("createroom/",views.createRoom,name="createRoom"),
    path('updateroom/<str:pk>/',views.updateRoom,name="updateRoom"),
    path('delete-room/<str:pk>/',views.deleteRoom,name="deleteRoom"),
    path('login_page/', views.login_page,name="login_page" ),
    path('logout/',views.logout_user,name="logout"),
    path('register/',views.register_user,name="register"),
    path("delete-message/<str:pk>",views.deleteMessage,name="delete-message"),
    path('user-profile/<str:pk>',views.userProfile,name='user-profile')
]