from rest_framework import serializers

from .models import Message, Conversation
from user.serializers import UserInfoSerializer


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        exclude = ("conversation",)


class ConversationListSerializer(serializers.ModelSerializer):
    initiator = UserInfoSerializer()
    receiver = UserInfoSerializer()
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ["id", "initiator", "receiver", "last_message"]

    def get_last_message(self, instance):
        message = instance.message_set.first()
        return MessageSerializer(instance=message)


class ConversationSerializer(serializers.ModelSerializer):
    initiator = UserInfoSerializer()
    receiver = UserInfoSerializer()
    message_set = MessageSerializer(many=True)

    class Meta:
        model = Conversation
        fields = ["id", "initiator", "receiver", "message_set"]
