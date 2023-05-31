from django.urls import path
from . import views

urlpatterns = [
    path('login', views.Login.as_view()),
    path('user/info', views.UserInfo.as_view()),
    path('home_data/', views.DashboardView.as_view()),
    # path('products/<pk>[0-9]+/', views.ProductDetail.as_view()),
    path('passports/', views.PassportList.as_view()),
    path('managers/', views.ManagerList.as_view()),
    path('managers/auth/', views.ManagerAuth.as_view()),
    path('records/', views.RecordList.as_view()),
    path('cameras/', views.CameraList.as_view()),
    path('projects/', views.ProjectList.as_view()),
    path('passports/<pk>/', views.PassportDetail.as_view()),
]
