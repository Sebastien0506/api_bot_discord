# api/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from discord_bot.models import PendingAction
from rest_framework import status

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
