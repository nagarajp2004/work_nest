from django.urls import path,include
from . import views  # Import your views
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet

# Create the DRF router for API views
router = DefaultRouter()
router.register(r'tasks', TaskViewSet)  # /tasks/ will now be available via the API

# Add your normal Django routes for views
urlpatterns = [
    path('register/', views.register, name='register'),  # Normal Django view
    path('', views.task_list, name='task_list'),  # Normal Django view
    path('task_create/', views.task_create, name="task_create"),  # Normal Django view
    path('task/<int:pk>/edit/', views.task_update, name='task_update'),  # Normal Django view
    path('task/<int:pk>/delete/', views.task_delete, name='task_delete'),  # Normal Django view
]

# Add the DRF routes under a /api/ prefix to distinguish them from the normal Django views
urlpatterns += [
    path('api/', include(router.urls))  # Add API routes under the /api/ prefix
]
