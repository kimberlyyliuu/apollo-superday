from django.urls import path
from . import views

urlpatterns = [
    path('vehicle', views.VehicleListCreate.as_view(), name='vehicle-list-create'),
    path('vehicle/<str:vin>', views.VehicleDetail.as_view(), name='vehicle-detail'),
]