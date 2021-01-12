from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializer, LoginSerializer, RefreshTokenSerializer

def send_activation_mail(user):
    code = user.create_activation_code()
    send_mail('Activation Account', f'Youre Successfully Registered. Please Activate Your Account by Following This Link http://127.0.0.1:8000/account/activate/{code}/', 'nurs@email.com', [user.email, ])



class RegisterView(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            send_activation_mail(user)
            return Response(serializer.data)
        return Response("Account Created")


class ActivationView(APIView):
    def get(self, request, activation_code):
        User = get_user_model()
        user = get_object_or_404(User, activation_code=activation_code)
        user.activate_with_code(activation_code)
        return Response('Ваш аккаунт успешно активирован')


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


class TokenRefresh(TokenRefreshView):
    serializer_class = RefreshTokenSerializer
    token_refresh = TokenRefreshView.as_view()


class LogoutView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)