from django.urls import path
from .apiviews import UsersView, get_logged_user, CreateUserView, SendFriendRequest, GetFriends,\
    GetReceivedRequests, GetSentRequests, RespondeRequest,\
    GetChat, SendMessage, GetChats, GetPublications, CreatePublication,\
    LikePublication, CancelRequest, CheckNewMessages, ChangePerfilPicture, GetUser, UpdatePassword, UpdateUserInfo
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path("api/users", UsersView.as_view(), name="users"),
    path("api/login", obtain_jwt_token, name="login"),
    path("api/get-logged-user/", get_logged_user, name="get-logged-user"),
    path("api/create-user", CreateUserView.as_view(), name="create-user"),
    path("api/change-perfil-picture", ChangePerfilPicture.as_view()),
    path("api/send-friend-request/", SendFriendRequest.as_view(), name="send-friend-request"),
    path("api/get-friends", GetFriends.as_view(), name="get-friends"),
    path("api/get-received-requests", GetReceivedRequests.as_view()),
    path("api/get-sent-requests", GetSentRequests.as_view()),
    path("api/responde-request", RespondeRequest.as_view()),
    path("api/cancel-request", CancelRequest.as_view()),
    path("api/get-chat", GetChat.as_view()),
    path("api/get-chats", GetChats.as_view()),
    path("api/send-message", SendMessage.as_view()),
    path("api/check-new-messages", CheckNewMessages.as_view()),
    path("api/get-publications", GetPublications.as_view()),
    path("api/create-publication", CreatePublication.as_view()),
    path("api/like-publication", LikePublication.as_view()),
    path("api/get-user", GetUser.as_view()),
    path("api/update-user-info", UpdateUserInfo.as_view()),
    path("api/update-user-password", UpdatePassword.as_view()),
]