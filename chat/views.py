from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from django.db.models import Q

from . import serializers
from .models import Conversation
from user.models import User


# Create your views here.
class StartConversationAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ConversationSerializer

    def create(self, request, receiver_id):
        try:
            receiver = User.objects.get(id=receiver_id)
        except User.DoesNotExist:
            return Response(
                {"detail": "You cannot start a conversation with a non existent user"}
            )

        conversation = Conversation.objects.filter(
            Q(initiator=request.user, receiver=receiver)
            | Q(initiator=receiver, receiver=request.user)
        )

        if conversation.exists():
            serializer = self.serializer_class(conversation)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            conversation = Conversation.objects.create(
                initiator=request.user, receiver=receiver
            )
            serializer = self.serializer_class(conversation)
            return Response(serializer.data, status=status.HTTP_200_OK)


start_conversation_view = StartConversationAPIView.as_view()


class GetConversationAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ConversationSerializer

    def retrieve(self, _, conversation_id):
        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            return Response({"detail": "This Conversation does not exist"})

        serializer = self.serializer_class(conversation)
        return Response(serializer.data, status=status.HTTP_200_OK)


get_conversation_view = GetConversationAPIView.as_view()


class GetConversationListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ConversationListSerializer

    def list(self, request):
        conversation_list = Conversation.objects.filter(
            Q(initiator=request.user) | Q(receiver=request.user)
        )

        serializer = self.serializer_class(conversation_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


get_conversation_list_view = GetConversationListAPIView.as_view()
