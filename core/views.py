# views.py
from rest_framework import viewsets, status
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from .models import CustomUser
from a_base.models import Subscription
from .serializers import RegisterSerializer, CustomTokenObtainPairSerializer, CustomUserPrivateSerializer, CustomUserPublicSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import PermissionDenied
from patients.models import Patient


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return CustomUserPublicSerializer
        
        # Для детального просмотра проверяем права
        if self.request.user.is_staff or self.request.user.is_superuser:
            return CustomUserPrivateSerializer
        
        # Для собственного профиля
        if self.action in ['retrieve', 'update', 'partial_update']:
            obj = self.get_object()
            if obj == self.request.user:
                return CustomUserPrivateSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Для обычных пользователей показываем только свой профиль
        if not (self.request.user.is_staff or self.request.user.is_superuser):
            queryset = queryset.filter(id=self.request.user.id)
        return queryset

    def get_object(self):
        obj = super().get_object()
        
        # Дополнительная проверка прав для детального просмотра
        if not (self.request.user.is_staff or 
                self.request.user.is_superuser or 
                obj == self.request.user):
            raise PermissionDenied("У вас нет прав доступа к этому профилю")
        return obj


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.subscription = Subscription.objects.get(name_ru="Базовая")
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
