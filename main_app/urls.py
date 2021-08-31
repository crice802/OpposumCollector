from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    path('about/', views.about, name='about'),
    
    path('opposums/', views.opposums_index, name='opposums_index'),
    
    path('opposums/<int:opposum_id>/', views.opposums_detail, name='opposums_detail'),

    path('opposums/create/', views.OpposumCreate.as_view(), name='opposums_create'),

    path('opposums/<int:pk>/update/', views.OpposumDelete.as_view(), name='opposums_delete'),

    path('opposums/<int:pk>/update/', views.OpposumUpdate.as_view(), name='opposums_update'),

    path('opposums/<int:opposum_id>/add_feeding/', views.add_feeding, name='add_feeding'),

    path('toys/create/', views.ToyCreate.as_view(), name='toys_create'),

    path('toys/<int:pk>/', views.ToyDetail.as_view(), name='toys_detail'),
  
    path('toys/', views.ToyList.as_view(), name='toys_index'),

    path('toys/<int:pk>/update/', views.ToyUpdate.as_view(), name='toys_update'),
  
    path('toys/<int:pk>/delete/', views.ToyDelete.as_view(), name='toys_delete'),

    path('opposums/<int:opposum_id>/add_feeding/', views.add_feeding, name='add_feeding'),
# associate a toy with a opposum (M:M)
    path('opposums/<int:opposum_id>/assoc_toy/<int:toy_id>/', views.assoc_toy, name='assoc_toy'),
]
