# api/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from discord_bot.models import PendingAction
from rest_framework import status
from discord_bot.services.generate_audio_message_service import generate_audio_message_service

@api_view(["POST"])
def join_voice_view(request):
    #On récupère les données de la requête
    user_id = request.data.get("user_id")
    channel_id = request.data.get("channel_id")
    
    # Si channel_id est manquant on renvoie un message d'erreur
    if not channel_id : 
        return Response({"error" : "channel_id manquant"}, status=status.HTTP_400_BAD_REQUEST)
    
    #Si user_id est manquant on renvoie un message d'erreur
    if not user_id : 
        return Response({"error" : "user_id manquant"}, status=status.HTTP_400_BAD_REQUEST)
    
    #Si tous est OK on crée un object PendingAction
    PendingAction.objects.create(
        action="join_voice",
        channel_id=channel_id,
        user_id=user_id,
    )
    return Response({
        "status": "ok",
        "message" : "Action enregistrée"
    })

@api_view(["POST"])
def voice_message(request):
    payload = request.data.get("payload")

    if not payload or "message" not in payload:
        return Response({"error": "Aucun message"}, status=400)

    message = payload["message"]

    channel_id = int(request.data.get("channel_id"))
    user_id = int(request.data.get("user_id"))

    PendingAction.objects.create(
        action="voice_message",
        channel_id=channel_id,
        user_id=user_id,
        payload={
            "message": message
        }
    )

    return Response({"status": "ok"})
