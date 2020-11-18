from .serializers import UserSerializer, CreateUserSerializer, FriendsSerializer, ReceivedRequestsSerializer,\
    SentRequestsSerializer, MessageSerializer, ChatSerializer, PublicationSerializer
from .models import User, UserSystem, Friend, ReceivedRequest, SentRequest, Chat, Message, Publication, Like
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import permissions
from django.db.models.signals import post_save
from django.dispatch import receiver
from .forms import ChangePerfilPictureForm
from cloudinary.uploader import upload
from django.contrib.auth import authenticate

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


class ChangePerfilPicture(APIView):
    def post(self, request):
        print(request.data)
        print(request.POST, request.FILES)
        form = ChangePerfilPictureForm(request.FILES['perfil_picture'])
        form.instance = request.user
        print(f"Aui esta {request.FILES['perfil_picture']}")
        #upload(request.FILES['perfil_picturea'])
        #print(form.is_valid())
        if form.is_valid():
            print("esta tudo bem.")
            print(form)
            form.save()
        else:
            print(form.errors)
        user = request.user
        user.perfil_picture = request.FILES['perfil_picture']
        user.save()
        return Response({})


@api_view(["GET"])
def get_logged_user(request):
    user = UserSerializer(request.user)
    return Response(user.data)


class CreateUserView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        user = CreateUserSerializer(data=request.data["data"])
        print(request.data)
        if user.is_valid():
            print(user.instance)
            user.save()
            return Response(user.data)

        else:
            print(f"Nao valido {user.errors}")
        return Response(user.errors)



class UpdateUserInfo(APIView):
    def post(self, request):
        print(request.data)
        user_authentication = authenticate(email=request.user.email, password=request.data["password"])
        if user_authentication:
            user = request.user
            user.username = request.data["username"]
            user.email = request.data["email"]
            user.save()
            return Response({"status": "Update feito"})
        return Response({"error": "Verifique a sua senha e tenta novamente"})


class UpdatePassword(APIView):
    def post(self, request):
        print(request.data)
        user_authentication = authenticate(email=request.user.email, password=request.data["old_password"])
        if user_authentication:
            user = request.user
            user.set_password(request.data["new_password"])
            user.save()
            return Response({"status": "Senha alterada"})
        return Response({"error": "Senha errada, verifique e tenta novamente"})


class GetUser(APIView):
    permission_classes = (permissions.AllowAny, )
    def get(self, request):
        user = User.objects.get(long_id=request.GET.get("user"))
        user = UserSerializer(user)
        return Response(user.data)



class SendFriendRequest(APIView):
    def post(self, request):
        user_system = UserSystem.objects.get(user=request.user)
        receiver = User.objects.get(long_id=request.data["user"])
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
        print(request.data)
        received_request = ReceivedRequest.objects.get(long_id=request.data["request"])
        sender = received_request.sender
        sender_system = UserSystem.objects.get(user=sender)
        print(sender)
        if request.data["response"]:
            print("Aceitar")
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


class CancelRequest(APIView):
    def post(self, request):
        print(request.data)
        sent_request = SentRequest.objects.get(long_id=request.data["request"])

        print(sent_request.receiver)
        receiver_user = sent_request.receiver
        receiver_system = UserSystem.objects.get(user=receiver_user)

        received_request = receiver_system.receivedrequest_set.get(sender=request.user)

        # Deleting the sent request and received recquest
        sent_request.delete()
        received_request.delete()
        return Response({"status": "Cancelado"})


class GetChat(APIView):
    def get(self, request):
        user_system = UserSystem.objects.get(user=request.user)

        print(request.GET.get("from"))
        data = {}
        if request.GET.get("from") == "user":
            receiver_user = User.objects.get(long_id=request.GET.get("user"))
            if user_system.chat_set.filter(receiver=receiver_user).exists():
                print("Existe")
                chat = user_system.chat_set.get(receiver=receiver_user)
                print(chat.message_set.all())
                messages = chat.message_set.all()
                messages = MessageSerializer(messages, many=True)
                data["messages"] = messages.data
                data["chat"] = ChatSerializer(chat).data

                # Cleaning new messages
                chat.new_messages = 0
                chat.save()
            else:
                print("Nao existe")
                data = {"status": "chat nao criado ainda", "user": UserSerializer(receiver_user).data}

        else:
            chat = Chat.objects.get(long_id=request.GET.get("user"))
            messages = chat.message_set.all()
            messages = MessageSerializer(messages, many=True)
            data["messages"] = messages.data
            
            # Cleaning new messages
            chat.new_messages = 0
            chat.save()

            chat = ChatSerializer(chat)
            data["chat"] = chat.data
        return Response(data)


class GetChats(APIView):
    def get(self, request):
        user_system = UserSystem.objects.get(user=request.user)
        chats = user_system.chat_set.all().order_by("-message__sent_day")
        chats_ids = []
        for chat in chats:
            if chat in chats_ids:
                pass
            else:
                chats_ids.append(chat)
        chats = chats_ids
        chats = ChatSerializer(chats, many=True)
        return Response(chats.data)


class SendMessage(APIView):
    def post(self, request):
        user_system = UserSystem.objects.get(user=request.user)
        print(request.data)
        if request.data["from"] == "user":

            receiver_user = User.objects.get(long_id=request.data["model"])
            receiver_system = UserSystem.objects.get(user=receiver_user)
            if not user_system.chat_set.filter(receiver=receiver_user).exists():

                # Creating chat for the current user
                user_chat = Chat(user_system=user_system, receiver=receiver_user)
                user_chat.save()

                # Create chat for the receiver user

                receiver_chat = Chat(user_system=receiver_system, receiver=request.user)
                receiver_chat.save()

            else:
                user_chat = user_system.chat_set.get(receiver=receiver_user)
                receiver_chat = receiver_system.chat_set.get(receiver=request.user)

            print("Vem de user")
        else:
            print("Vem de chat")
            user_chat = Chat.objects.get(long_id=request.data["model"])
            receiver_user = user_chat.receiver
            receiver_system = UserSystem.objects.get(user=receiver_user)
            receiver_chat = receiver_system.chat_set.get(receiver=request.user)

        # Create the message for the current user
        message = Message(chat=user_chat, sender=request.user, message=request.data["message"])
        message.save()

        # Creating message for the receiver user
        message = Message(chat=receiver_chat, sender=request.user, message=request.data["message"])
        message.save()
        message = MessageSerializer(message)

        # Saving the last message
        user_chat.last_message = request.data["message"]
        user_chat.save()

        receiver_chat.last_message = request.data["message"]
        receiver_chat.new_messages += 1
        receiver_chat.save()
        return Response(message.data)


class CheckNewMessages(APIView):
    def get(self, request):
        print(request.GET.get("chat"))
        chat = Chat.objects.get(long_id=request.GET.get("chat"))
        print(len(chat.message_set.all()))
        if len(chat.message_set.all()) != int(request.GET.get("chat_length")):
            print("Messagens diferentes")
        messages = chat.message_set.all()[int(request.GET.get("chat_length")):]
        messages = MessageSerializer(messages, many=True)
        return Response(messages.data)


class GetPublications(APIView):
    def get(self, request):
        print(request.GET.get("from_user"))
        if request.GET.get("from_user") == "true":
            try:
                user = User.objects.get(long_id=request.GET.get("user"))
                user_system = UserSystem.objects.get(user=user)
                pubs = Publication.objects.filter(user_system=user_system).order_by("-pub_date")
                print(f"As pubs aqui {pubs}")
            except Exception as error:
                print(error)
        else:
            pubs = Publication.objects.all().order_by("-pub_date")
        
        for pub in pubs:
            print(pub.like_set.all())
        pubs = PublicationSerializer(pubs, many=True)

        return Response(pubs.data)


class CreatePublication(APIView):
    def post(self, request):
        print(request.data)
        user_system = UserSystem.objects.get(user=request.user)
        pub = Publication(user_system=user_system, context=request.data["context"])
        pub.save()
        pub = PublicationSerializer(pub)
        return Response(pub.data)


class LikePublication(APIView):
    def post(self, request):
        print(request.data["pub"])
        user_system = UserSystem.objects.get(user=request.user)
        pub = Publication.objects.get(long_id=request.data["pub"])
        if pub.like_set.filter(user_system=user_system).exists():
            print("Like ja dado")
            like = pub.like_set.get(user_system=user_system)
            like.delete()
            pub.likes -= 1
            pub.save()
        else:
            print("Novo")
            like = Like(user_system=user_system, publication=pub)
            like.save()
            pub.likes += 1
            pub.save()
        return Response({"likesNum": pub.likes})