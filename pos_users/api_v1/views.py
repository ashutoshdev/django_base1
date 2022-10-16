import logging

from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *

logger = logging.getLogger(__name__)


class UserSignupView(APIView):
    """
    Business User Signup API
    """
    serializer_class = UserSerializer

    def before_create_signal(self, request, *args, **kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        request.data['user'] = dict()
        request.data['user']['email'] = request.data.get('email')
        request.data['user']['first_name'] = request.data.get('first_name')
        request.data['user']['last_name'] = request.data.get('last_name')
        request.data['user']['password'] = request.data.get('password')
        request.data['is_business_owner'] = request.data.get(
            'is_business_owner', True)

    def post(self, request, *args, **kwargs):
        """
        UI request data mapping
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        self.before_create_signal(request, *args, **kwargs)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": True,
                 "message": "Successful"},
                status=status.HTTP_200_OK
            )
        return Response({"status": False, "message": serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    """
    User Login,
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        user = authenticate(request, username=request.data["email"],
                            password=request.data["password"])

        # Checking if user exist
        if user:
            response = user.application_details()
            return Response(response, status=status.HTTP_200_OK)
        return Response({'message': "Invalid credentials!"},
                        status=status.HTTP_400_BAD_REQUEST)


class Logout(APIView):
    """
    Logout API
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        AccessToken.objects.filter(user=request.user).delete()
        return Response({'message': 'Successfully logged out'},
                        status=status.HTTP_200_OK)
