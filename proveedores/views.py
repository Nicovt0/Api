from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class InfoProveedorAPIView(APIView):
    def post(self, request):
        data = request.data
        id_proveedor = data.get("id_proveedor")
        productos = data.get("productos")  # Lista de ID de producto
        cantidades = data.get("cantidades")  # Lista con la cantidad por producto

        if not (id_proveedor and productos and cantidades):
            return Response({"error": "Parámetros incompletos"}, status=status.HTTP_400_BAD_REQUEST)

        if len(productos) != len(cantidades):
            return Response({"error": "Longitud de productos y cantidades no coinciden"}, status=status.HTTP_400_BAD_REQUEST)

        response = []
        for producto_id, cantidad in zip(productos, cantidades):
            response.append({
                "proveedor_id": id_proveedor,
                "producto_id": producto_id,
                "cantidad": cantidad,
                "estado": "recibido"
            })

        return Response(response, status=status.HTTP_200_OK)