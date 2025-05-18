from django.urls import path
from .views import (
    CrearOrdenAPIView, 
    ObtenerOrdenAPIView, 
    EliminarOrdenAPIView,
    ModificarEstadoOrdenAPIView,
    )

urlpatterns = [
    path('orden/crear/', CrearOrdenAPIView.as_view()),
    path('orden/obtener/', ObtenerOrdenAPIView.as_view()),
    path('orden/eliminar/', EliminarOrdenAPIView.as_view()),
    path('orden/modificar-estado/', ModificarEstadoOrdenAPIView.as_view()),
]