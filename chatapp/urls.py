from django.urls import path
from .apiviews import UsersView, get_logged_user, CreateUserView
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path("api/users", UsersView.as_view(), name="users"),
    path("api/login", obtain_jwt_token, name="login"),
    path("api/get-logged-user/", get_logged_user, name="get-logged-user"),
    path("api/create-user", CreateUserView.as_view(), name="create-user")
]