from .serializers import UserSerializer, CreateUserSerializer
from .models import User, UserSystem, Friend, ReceivedRequest, SentRequest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import permissions
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User, dispatch_uid="user_signal")
def user_signal(sender, instance, **kwargs):
    try:
        user_system = UserSystem(user=instance)
        user_system.save()
    except:
        pass


class UsersView(APIView):
    def get(self, request):
        users = User.objects.all()
        users = UserSerializer(users, many=True)
        for c in range(10):
            print(users)
        return Response(users.data)


@api_view(["GET"])
def get_logged_user(request):
    user = UserSerializer(request.user)
    return Response(user.data)


class CreateUserView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        user = CreateUserSerializer(data=request.data)
        if user.is_valid():
            print(user.instance)
            user.save()
        return Response(user.data)

