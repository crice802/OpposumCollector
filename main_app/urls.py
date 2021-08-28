from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('opposums/', views.opposums_index, name='opposums_index'),
]
