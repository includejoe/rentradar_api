import uuid
from rest_framework import serializers

from user.models import User
from .models import Message, Conversation
from user.serializers import UserInfoSerializer


class UserID(serializers.Field):
    def to_representation(self, value):
        if isinstance(value, User):
            return str(value.id)
        return value


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        exclude = ("conversation",)


class GetMessageSerializer(serializers.ModelSerializer):
    sender = UserID()

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
        if message:
            return MessageSerializer(instance=message).data
        else:
            return None


class ConversationSerializer(serializers.ModelSerializer):
    initiator = UserInfoSerializer()
    receiver = UserInfoSerializer()
    message_set = MessageSerializer(many=True)

    class Meta:
        model = Conversation
        fields = ["id", "initiator", "receiver", "message_set"]
