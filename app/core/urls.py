from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from core import views

router = DefaultRouter()
router.register('categories',views.Categorie_EquipementViewSets, basename='Categorie_Equipements')
router.register('location', views.LoacationViewSets, basename='Location')

urlpatterns = [
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
    path('Adminpage/location/<int:pk>/', views.LoacationViewSets.as_view({'get':'list', 'delete':'destroy', 'put':'update'})),
    path('Adminpage/categories/<int:pk>/', views.Categorie_EquipementViewSets.as_view({'get':'list', 'delete':'destroy', 'put':'update'})),
    path('Adminpage/', include(router.urls))
]
