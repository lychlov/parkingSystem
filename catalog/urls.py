from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductList.as_view()),
    # path('products/<pk>[0-9]+/', views.ProductDetail.as_view()),
]
