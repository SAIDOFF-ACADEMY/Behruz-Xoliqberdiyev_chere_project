from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView, \
    UpdateAPIView, RetrieveAPIView, DestroyAPIView, RetrieveDestroyAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from users import models
from users import serializers


class UserList(ListAPIView):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()
    permission_classes = [IsAdminUser]


class UserDetail(RetrieveAPIView):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()
    permission_classes = [IsAdminUser]
    lookup_field = 'id'


class UserUpdateView(UpdateAPIView):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()
    permission_classes = [IsAdminUser]
    lookup_field = 'id'


class UserDeleteView(DestroyAPIView):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()
    permission_classes = [IsAdminUser]
    lookup_field = 'id'


class UserCreate(CreateAPIView):
    serializer_class = serializers.UserCreateSerializer
    queryset = models.User.objects.all()
    permission_classes = [IsAdminUser]


class UserContactView(ListAPIView):
    serializer_class = serializers.UserContactSerializer
    queryset = models.UserContactApplication.objects.all()
    permission_classes = [IsAdminUser]


class UserContactDetail(RetrieveDestroyAPIView):
    serializer_class = serializers.UserContactSerializer
    lookup_field = 'id'
    queryset = models.UserContactApplication.objects.all()
    permission_classes = [IsAdminUser]


class UserContactUpdate(UserUpdateView):
    serializer_class = serializers.UserContactUpdateSerializer
    lookup_field = 'id'
    queryset = models.UserContactApplication.objects.all()
    permission_classes = [IsAdminUser]


class UserLoginView(GenericAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(data, status=status.HTTP_200_OK)


