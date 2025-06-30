from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Proveedor, Prod_Proveedor, Orden, ProductoOrden
from django.utils.crypto import get_random_string
from datetime import datetime
from .mailjet import send_mailjet_email

class CrearOrdenAPIView(APIView):
    def post(self, request):
        data = request.data
        id_proveedor = data.get("id_proveedor")
        productos = data.get("productos")  # Lista de IDs
        cantidades = data.get("cantidades")  # Lista de cantidades

        print(f"{id_proveedor}, {productos}, {cantidades} ")
        print("paso fase 1")

        if not (id_proveedor and productos and cantidades):
            return Response({"error": "Parámetros incompletos"}, status=status.HTTP_400_BAD_REQUEST)
        print("paso fase 2")

        proveedor = Proveedor.objects.get(pk=id_proveedor)
        codigo_orden = get_random_string(length=10).upper()

        print(f"{proveedor}, {codigo_orden}")

        orden = Orden.objects.create(
            proveedor=proveedor,
            codigo=codigo_orden,
            estado='pendiente'
        )
        print("paso fase 3")

        total = 0
        detalle_producto = ""
        detalle_precio = ""
        detalle_subtotal = ""
        detalle_html = ""
        for pid, cant in zip(productos, cantidades):
            producto = Prod_Proveedor.objects.get(pk=pid)
            ProductoOrden.objects.create(orden=orden, producto=producto, cantidad=cant)
            subtotal = producto.precio * cant
            total += subtotal
            detalle_producto += f"\n -{producto.nombre_producto} (x{cant}) <br>"
            detalle_precio += f"\n ${producto.precio} <br>"
            detalle_subtotal += f"\n ${subtotal} <br>"

        mensaje = f"""
        Estimado/a {proveedor.nombre} {proveedor.apellido},

        Se ha generado una orden de compra (Código: {orden.codigo}) con fecha {orden.fecha.strftime('%Y-%m-%d')}.

        Productos solicitados:{detalle_producto}{detalle_precio}{detalle_subtotal}

        Total: ${total}

        Atentamente,
        Sistema de Órdenes
        """

        response = send_mailjet_email(
            to_email=proveedor.correo,
            name=f"{proveedor.nombre} {proveedor.apellido}",
            producto=detalle_producto,
            precio=detalle_precio,
            subtotal=detalle_subtotal,
            total=total,
            fecha=orden.fecha.strftime('%Y-%m-%d'),
            codigo=codigo_orden
        )

        send_mail(
            subject="Nueva Orden de Compra",
            message=mensaje,
            from_email="sistema@ordenes.com",
            recipient_list=[proveedor.correo],
            fail_silently=False
        )

        print("Status Code:", response["status_code"])
        print("Respuesta de Mailjet:", response["response"])

        return Response({
            "mensaje": "Orden creada y correo enviado.",
            "codigo_orden": orden.codigo,
            "total": total
        }, status=status.HTTP_201_CREATED)


class ObtenerOrdenAPIView(APIView):
    def post(self, request):
        codigo = request.data.get("codigo")
        try:
            orden = Orden.objects.get(codigo=codigo)
            productos = ProductoOrden.objects.filter(orden=orden)

            detalle = []
            for p in productos:
                detalle.append({
                    "producto": p.producto.nombre_producto,
                    "cantidad": p.cantidad,
                    "precio_unitario": p.producto.precio,
                    "subtotal": p.producto.precio * p.cantidad
                })

            return Response({
                "codigo": orden.codigo,
                "estado": orden.estado,
                "proveedor": {
                    "nombre": orden.proveedor.nombre,
                    "correo": orden.proveedor.correo,
                    "rut": f"{orden.proveedor.rut}-{orden.proveedor.dv}"
                },
                "fecha": orden.fecha,
                "productos": detalle
            }, status=status.HTTP_200_OK)
        except Orden.DoesNotExist:
            return Response({"error": "Orden no encontrada"}, status=status.HTTP_404_NOT_FOUND)


class ObtenerOrdenesAPIView(APIView):
    def post(self, request):
        id_proveedor = request.data.get("id_proveedor")
        try:
            proveedor = Proveedor.objects.get(id_proveedor=id_proveedor)
            ordenes = Orden.objects.filter(proveedor=proveedor)

            resultado = []
            for orden in ordenes:
                productos = ProductoOrden.objects.filter(orden=orden)
                detalle = []
                for p in productos:
                    detalle.append({
                        "producto": p.producto.nombre_producto,
                        "cantidad": p.cantidad,
                        "precio_unitario": p.producto.precio,
                        "subtotal": p.producto.precio * p.cantidad
                    })
                resultado.append({
                    "codigo": orden.codigo,
                    "estado": orden.estado,
                    "proveedor": {
                        "nombre": proveedor.nombre,
                        "correo": proveedor.correo,
                        "rut": f"{proveedor.rut}-{proveedor.dv}"
                    },
                    "fecha": orden.fecha,
                    "productos": detalle
                })
            return Response(resultado, status=status.HTTP_200_OK)
        except Proveedor.DoesNotExist:
            return Response({"error": "Proveedor no encontrado"}, status=status.HTTP_404_NOT_FOUND)


class EliminarOrdenAPIView(APIView):
    def post(self, request):
        codigo = request.data.get("codigo")
        try:
            orden = Orden.objects.get(codigo=codigo)
            orden.delete()
            return Response({"mensaje": "Orden eliminada correctamente"}, status=status.HTTP_200_OK)
        except Orden.DoesNotExist:
            return Response({"error": "Orden no encontrada"}, status=status.HTTP_404_NOT_FOUND)


class ModificarEstadoOrdenAPIView(APIView):
    def post(self, request):
        codigo = request.data.get("codigo")
        nuevo_estado = request.data.get("estado")

        if not codigo or not nuevo_estado:
            return Response(
                {"error": "Debe enviar codigo y estado"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            orden = Orden.objects.get(codigo=codigo)
        except Orden.DoesNotExist:
            return Response(
                {"error": "Orden no encontrada"},
                status=status.HTTP_404_NOT_FOUND
            )

        orden.estado = nuevo_estado
        orden.save()

        return Response(
            {
                "mensaje": "Estado de la orden actualizado",
                "codigo": orden.codigo,
                "nuevo_estado": orden.estado
            },
            status=status.HTTP_200_OK
        )