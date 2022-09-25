from user.serializers import UserSerializer
from rest_framework import generics


class CreateUserApiView(generics.CreateAPIView):
    serializer_class = UserSerializer
