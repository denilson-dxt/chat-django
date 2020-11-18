from rest_framework import serializers
from .models import User, Friend, ReceivedRequest, SentRequest, Message, Chat, Publication, Like, UserSystem


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserSystemSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserSystem
        fields = "__all__"


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "username", "password"]

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
            instance.save()
        instance.save()
        return instance


class FriendsSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Friend
        fields = "__all__"


class ReceivedRequestsSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = ReceivedRequest
        fields = "__all__"


class SentRequestsSerializer(serializers.ModelSerializer):
    receiver = UserSerializer(read_only=True)

    class Meta:
        model = SentRequest
        fields = "__all__"


class ChatSerializer(serializers.ModelSerializer):
    receiver = UserSerializer(read_only=True)

    class Meta:
        model = Chat
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    chat = ChatSerializer(read_only=True)
    class Meta:
        model = Message
        fields = "__all__"


class LikeSerializer(serializers.ModelSerializer):
    user_system = UserSystemSerializer(read_only=True)
    class Meta:
        model = Like
        fields = ["user_system"]


class PublicationSerializer(serializers.ModelSerializer):
    user_system = UserSystemSerializer(read_only=True)
    like_set = LikeSerializer(read_only=True, many=True, required=False)

    class Meta:
        model = Publication
        fields = ["context", "like_set", "likes", "pub_date", "long_id", "user_system"]
