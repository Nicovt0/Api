from django.urls import path
from .views import (
    CrearOrdenAPIView, 
    ObtenerOrdenAPIView, 
    EliminarOrdenAPIView,
    ModificarEstadoOrdenAPIView,
    ObtenerOrdenesAPIView,
    )

urlpatterns = [
    path('orden/crear/', CrearOrdenAPIView.as_view()),
    path('orden/obtener/', ObtenerOrdenAPIView.as_view()),
    path('orden/eliminar/', EliminarOrdenAPIView.as_view()),
    path('orden/modificar-estado/', ModificarEstadoOrdenAPIView.as_view()),
    path('ordenes/obtener/', ObtenerOrdenesAPIView.as_view()),
]