from chatapp.serializers import  UserSerializer


def my_jwt_response_handler(token, user, request=None):
    return {
        "token": token,
        "user": UserSerializer(user, context={"request": request}).data
    }