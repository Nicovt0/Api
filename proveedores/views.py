from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Proveedor, Prod_Proveedor

class InfoProveedorAPIView(APIView):
    def post(self, request):
        data = request.data
        id_proveedor = data.get("id_proveedor")
        productos = data.get("productos")  # Lista de IDs de producto

        if not id_proveedor or not productos:
            return Response({"error": "Parámetros incompletos"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            proveedor = Proveedor.objects.get(id_proveedor=id_proveedor)
        except Proveedor.DoesNotExist:
            return Response({"error": "Proveedor no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        productos_info = []
        for producto_id in productos:
            try:
                producto = Prod_Proveedor.objects.get(id_producto=producto_id, id_proveedor=proveedor)
                productos_info.append({
                    "nombre_producto": producto.nombre_producto
                })
            except Prod_Proveedor.DoesNotExist:
                productos_info.append({
                    "error": f"Producto con ID {producto_id} no encontrado para este proveedor"
                })

        response = {
            "nombre_proveedor": f"{proveedor.nombre} {proveedor.apellido}",
            "productos": productos_info
        }

        return Response(response, status=status.HTTP_200_OK)