# views.py
from rest_framework import viewsets, status
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from .models import CustomUser
from a_base.models import Subscription
from .serializers import CustomUserSerializer, RegisterSerializer, CustomTokenObtainPairSerializer, CustomUserShortSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import IsAdminOrSelf, IsAdminOrReadOnlyForSelf
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import action
from patients.models import Patient


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnlyForSelf]

    def get_serializer_class(self):
        # Для списка пользователей используем укороченный сериализатор
        if self.action == 'list':
            return CustomUserShortSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        # Для не-админов показываем только их собственный профиль
        if not self.request.user.is_staff:
            return CustomUser.objects.filter(id=self.request.user.id)
        return super().get_queryset()

    @action(detail=False, methods=['get'])
    def me(self, request):
        # Эндпоинт для получения текущего пользователя
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        # Разрешаем удаление только администратору или самому пользователю
        instance = self.get_object()
        if not (request.user.is_staff or instance == request.user):
            return Response(
                {'detail': 'У вас нет прав для удаления этого пользователя.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)

class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.subscription = Subscription.objects.get(id=1)
        user.activate_subscription()
        Patient.objects.create(user=user)

        return Response(
            {"message": "Пользователь успешно зарегистрирован."},
            status=status.HTTP_201_CREATED
        )
    
# Представление для получения JWT-токена с кастомными полями
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class ConfirmEmailView(APIView):

    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')

        if not email or not code:
            return Response({"error": "Email и код подтверждения обязательны."}, status=status.HTTP_400_BAD_REQUEST)

        user = CustomUser.objects.filter(email=email).first()
        if not user:
            return Response({"error": "Пользователь не найден."}, status=status.HTTP_404_NOT_FOUND)

        if user.is_active:
            return Response({"message": "Email уже подтвержден."}, status=status.HTTP_200_OK)

        if user.is_confirmation_code_valid(code):
            user.confirmation_code = None
            user.confirmation_code_created_at = None
            user.email_verified = True
            user.save()
            return Response({"message": "Email успешно подтвержден."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Неверный или просроченный код подтверждения."}, status=status.HTTP_400_BAD_REQUEST)
