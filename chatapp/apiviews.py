from .serializers import UserSerializer, CreateUserSerializer, FriendsSerializer, ReceivedRequestsSerializer, SentRequestsSerializer
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
        #user_system = UserSystem.objects.get(user=request.user)
        users = []
        for user in User.objects.all():
            if user != request.user:
                user_system = UserSystem.objects.get(user=user)
                print(f" amigos {user_system.friend_set.filter(user=request.user).exists()}")
                print(f" recebido {user_system.receivedrequest_set.filter(sender=request.user).exists()}")
                if not user_system.friend_set.filter(user=request.user).exists():
                    print(f"Nao sao {user}")
                if not user_system.sentrequest_set.filter(receiver=request.user).exists() \
                        and not user_system.receivedrequest_set.filter(sender=request.user).exists()\
                        and not user_system.friend_set.filter(user=request.user).exists():
                    print(f"eita{user}")
                    users.append(user)
                else:
                    pass
        users = UserSerializer(users, many=True)

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


class SendFriendRequest(APIView):
    def post(self, request):
        user_system = UserSystem.objects.get(user=request.user)
        receiver = User.objects.get(long_id=request.data["receiver"])
        if user_system.sentrequest_set.filter(receiver=receiver).exists() or \
                user_system.receivedrequest_set.filter(sender=receiver).exists():
            return Response({"status": "Pedido ja existente or recusado"})
        print(user_system.sentrequest_set.all())
        # Saving on the current user
        send_request = SentRequest(user_system=user_system, receiver=receiver)
        send_request.save()

        # Saving on the receiver
        receiver_system = UserSystem.objects.get(user=receiver)
        received_request = ReceivedRequest(user_system=receiver_system, sender=request.user)
        received_request.save()
        return Response({"status": "enviado"})


class GetFriends(APIView):
    def get(self, request):
        user_system = UserSystem.objects.get(user=request.user)
        friends = Friend.objects.filter(user_system=user_system)
        friends = FriendsSerializer(friends, many=True)
        return Response(friends.data)


class GetReceivedRequests(APIView):
    def get(self, request):
        user_system = UserSystem.objects.get(user=request.user)
        requests = ReceivedRequest.objects.filter(user_system=user_system, acepted=False, denied=False)
        requests = ReceivedRequestsSerializer(requests, many=True)
        return Response(requests.data)


class GetSentRequests(APIView):
    def get(self, request):
        user_system = UserSystem.objects.get(user=request.user)
        requests = SentRequest.objects.filter(user_system=user_system, acepted=False, denied=False)
        requests = SentRequestsSerializer(requests, many=True)
        return Response(requests.data)


class RespondeRequest(APIView):
    def post(self, request):
        user_system = UserSystem.objects.get(user=request.user)
        received_request = ReceivedRequest.objects.get(long_id=request.data["request"])
        sender = received_request.sender
        sender_system = UserSystem.objects.get(user=sender)
        print(sender)
        if request.data["response"]:
            # Resquest accepted
            # Saving on the current user
            friend = Friend(user_system=user_system, user=sender)
            friend.save()

            # Saving on the sender

            sender_system = UserSystem.objects.get(user=sender)
            friend = Friend(user_system=sender_system, user=request.user)
            friend.save()

            # Changing the request state of the sender
            received_request.acepted = True
            received_request.save()

            # Changing the request state of the current user
            sent_request = sender_system.sentrequest_set.get(receiver=request.user)
            sent_request.acepted = True
            sent_request.save()

        else:
            received_request.denied = True
            received_request.save()
            sent_request = sender_system.sentrequest_set.get(receiver=request.user)
            sent_request.denied = True
            sent_request.save()
            print("Eita")

        return Response({})


class GetChat(APIView):
    def get(self, request):
        print("Obetendo chat")
        print(request.GET.get("user"))
        return Response({})