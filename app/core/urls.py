from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from core import views
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'users', views.UserViewsets, basename='profiles-user')
router.register(r'admins', views.AdminViewsets, basename='profiles-admin')
router.register(r'principalmanagers', views.PrincipalmanagerViewsets, basename='profiles-principal')
router.register(r'Allocationmanager', views.AllocationmanagerViewsets, basename='profiles-allocationmanager')
router.register(r'Student', views.StudentViewsets, basename='profiles-student')
router.register(r'Researcher', views.ResearcherViewsets, basename='profiles-researcher')


urlpatterns = [
    *static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT),
    # path('connecteduser/', views.ConnectedUserView.as_view(), name='connected-user'),
    path('profiles/', include(router.urls)),
    path('login/', views.UserLoginApiView.as_view()),
    path('location/', views.LoacationApiView.as_view()),
    path('location/<int:pk>/', views.LoacationApiView.as_view()),
    path('categories/', views.Categorie_EquipementApiView.as_view()),
    path('categories/<int:pk>/', views.Categorie_EquipementApiView.as_view()),
    path('stock/', views.StockApiView.as_view()),
    path('stock/<int:pk>/', views.StockApiView.as_view()),
    path('equipement/', views.EquipementApiview.as_view()),
    path('equipement/<int:pk>/', views.EquipementApiview.as_view()),
    path('affectation', views.AffectationApiView.as_view()),
    path('affectation/<int:pk>', views.AffectationApiView.as_view()),
    path('inventory/', views.InventoryApiView.as_view()),
    path('inventory/<int:pk>', views.InventoryApiView.as_view()),
    path('allocation/', views.AllocationEquipementsApiView.as_view()),
    path('allocation/<int:pk>/', views.AllocationEquipementsApiView.as_view()),
    path('allocate/', views.AllocateEquipementsApiView.as_view()),
    path('allocate/<int:pk>', views.AllocateEquipementsApiView.as_view()),
    path('acceptrequest/', views.AcceptrequestApiView.as_view()),
    path('acceptrequest/<int:pk>/', views.AcceptrequestApiView.as_view()),
    path('notificationstd', views.NotificationStudentApiView.as_view()),
    path('notificationstd/<int:pk>/', views.NotificationStudentApiView.as_view()),
    path('notificationmng', views.NotificationManagerApiView.as_view()),
    path('notificationmng/<int:pk>/', views.NotificationManagerApiView.as_view()),
    path('reserved/', views.ReservedEquipementsApiView.as_view()),
    path('reserved/<int:pk>', views.ReservedEquipementsApiView.as_view()),
    path('return/', views.ReturnEquipementApiView.as_view()),
    path('return/<int:pk>', views.ReturnEquipementApiView.as_view()),
    path('allocatehpc/', views.AllocateHPCApiView.as_view()),
    path('allocatehpc/<int:pk>', views.AllocateHPCApiView.as_view()),
    path('reservedhpc/', views.ReservedHPCApiView.as_view()),
    path('reservedhpc/<int:pk>', views.ReservedHPCApiView.as_view()),
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
