from django.urls import path
from .apiviews import UsersView, get_logged_user, CreateUserView, SendFriendRequest, GetFriends,\
    GetReceivedRequests, GetSentRequests, RespondeRequest, GetChat
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path("api/users", UsersView.as_view(), name="users"),
    path("api/login", obtain_jwt_token, name="login"),
    path("api/get-logged-user/", get_logged_user, name="get-logged-user"),
    path("api/create-user", CreateUserView.as_view(), name="create-user"),
    path("api/send-friend-request/", SendFriendRequest.as_view(), name="send-friend-request"),
    path("api/get-friends", GetFriends.as_view(), name="get-friends"),
    path("api/get-received-requests", GetReceivedRequests.as_view()),
    path("api/get-sent-requests", GetSentRequests.as_view()),
    path("api/responde-request", RespondeRequest.as_view()),
    path("api/get-chat", GetChat.as_view()),
]