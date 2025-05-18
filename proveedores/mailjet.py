from mailjet_rest import Client
import os
from dotenv import load_dotenv
load_dotenv()

def send_mailjet_email(to_email, name, producto, precio, subtotal, total, fecha, codigo):
    """
    Envía un correo usando Mailjet con plantilla y variables dinámicas.

    Args:
        to_email (str): Correo del destinatario.
        name (str): Nombre del usuario.
        producto (str): Nombre del producto.
        precio (float): Precio del producto.
        subtotal (float): Subtotal de la orden.
        total (float): Total de la orden.
        fecha (str): Fecha de la orden.
        codigo (str): Código de la orden.
    """
    api_key = os.environ['MJ_APIKEY_PUBLIC']
    api_secret = os.environ['MJ_APIKEY_PRIVATE']
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')

    data = {
        'Messages': [
            {
                "From": {
                    "Email": "beig.techsolutions@gmail.com",
                    "Name": "Beig Tech Solutions"
                },
                "To": [
                    {
                        "Email": to_email,
                    }
                ],
                "TemplateID": 6993882,
                "TemplateLanguage": True,
                "Variables": {
                    "name": name,
                    "producto": producto,
                    "precio": precio,
                    "subtotal": subtotal,
                    "total": total,
                    "fecha": fecha,
                    "codigo": codigo,
                }
            }
        ]
    }

    result = mailjet.send.create(data=data)
    return {
        "status_code": result.status_code,
        "response": result.json()
    }