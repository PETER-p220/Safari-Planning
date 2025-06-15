from . import views
from .views import FormDataView
from .views import LoginView
from .views import BookingCreateView
from rest_framework.routers import DefaultRouter
from .views import SafariPackageViewSet
from django.urls import path,include

router = DefaultRouter()

urlpatterns = [
    path('',views.index,name='index'),
    path('api/register', FormDataView.as_view(), name='form-data'),
    path('api/login', LoginView.as_view(), name='login'),
    path('api/bookings', BookingCreateView.as_view(), name='booking-create'),
    path('api/safari-packages',SafariPackageViewSet.as_view({'get': 'list', 'post': 'create'}), name='safari-package-list-create'),
]
