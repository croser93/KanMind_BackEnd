from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import RegistrationSerializer, LoginSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import status

class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        data = {}
        if serializer.is_valid():
            saved_account = serializer.save()
            token, created = Token.objects.get_or_create(user=saved_account)
            data = {
                'token'     :   token.key,
                'fullname'  :   saved_account.get_full_name(),
                'email'     :   saved_account.email,
                'id'        :   saved_account.id
            }
        else:
             return Response(serializer.errors, status=400)

        return Response(data, status=201)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        data = {}
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            data = {
                'token'     : token.key,
                'fullname'  : user.get_full_name(),
                'email'     : user.email,
                'id'        : user.id
            }
        else:
             return Response(serializer.errors, status=400)

        return Response(data, status=200)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({'detail' :"Logout erfolgreich. Token wurde gelöscht."}, status=200)
