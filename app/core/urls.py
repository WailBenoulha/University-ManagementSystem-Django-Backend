from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from core import views


urlpatterns = [
    path('login/', views.UserLoginApiView.as_view()),
    path('stock/', views.StockApiView.as_view()),
    path('stock/<int:pk>/', views.StockApiView.as_view()),
    path('affectation', views.AffectationApiView.as_view()),
    path('affectation/<int:pk>', views.AffectationApiView.as_view()),
    path('inventory/', views.InventoryApiView.as_view()),
    path('inventory/<int:pk>', views.InventoryApiView.as_view()),
    path('allocation/', views.AllocationApiView.as_view()),
    path('allocation/<int:pk>', views.AllocationApiView.as_view()),
    path('equipement/', views.EquipementApiview.as_view()),
    path('equipement/<int:pk>/', views.EquipementApiview.as_view()),
    path('location/', views.LoacationApiView.as_view()),
    path('location/<int:pk>/', views.LoacationApiView.as_view()),
    path('categories/', views.Categorie_EquipementApiView.as_view()),
    path('categories/<int:pk>/', views.Categorie_EquipementApiView.as_view()),
    path('allocate/', views.AllocateApiView.as_view()),
    path('allocate/<int:pk>/', views.AllocateApiView.as_view()),
    path('notificationstd', views.NotificationStudentApiView.as_view()),
    path('notificationstd/<int:pk>/', views.NotificationStudentApiView.as_view()),
    path('notificationmng', views.NotificationManagerApiView.as_view()),
    path('notificationmng/<int:pk>/', views.NotificationManagerApiView.as_view()),
    path('acceptrequest/', views.AcceptrequestApiView.as_view()),
    path('acceptrequest/<int:pk>/', views.AcceptrequestApiView.as_view()),
    path('reservedequip/', views.ReservedEquipApiView.as_view()),
    path('reservedequip/<int:pk>/', views.ReservedEquipApiView.as_view()),
    path('returnequipement/', views.ReturnEquipementApiview.as_view()),
    path('returnequipement/<int:pk>/', views.ReturnEquipementApiview.as_view())
]
