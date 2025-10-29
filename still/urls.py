from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DynamicDataViewSet, TestView

router = DefaultRouter()
router.register(r'data', DynamicDataViewSet, basename='dynamicdata')

urlpatterns = [
    path('test/', TestView.as_view(), name='test_controller'),
    path('', include(router.urls)),
]
