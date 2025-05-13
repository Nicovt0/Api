from django.urls import path
from .views import InfoProveedorAPIView

urlpatterns = [
    path('info-proveedor/', InfoProveedorAPIView.as_view()),
]