from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['POST'])
def colorize(request):
    """
    Recibe una imagen en blanco y negro y responde con un mensaje de confirmación.
    Más adelante se implementará la lógica de colorización.
    """
    if 'image' not in request.FILES:
        return Response(
            {"error": "No se envió ninguna imagen"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Aquí se realizará el proceso de colorización en futuras iteraciones

    return Response({"message": "ok"}, status=status.HTTP_200_OK) 