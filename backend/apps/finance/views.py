from rest_framework import viewsets, permissions, status
from core.utils import api_response
from apps.authentication.permissions import IsAdmin
from .models import Payment
from .serializers import PaymentSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdmin()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.role == 'ADMIN':
            return Payment.objects.all()
        if user.role == 'STUDENT':
            return Payment.objects.filter(student__user=user)
        if user.role == 'PARENT':
            return Payment.objects.filter(student__parents__user=user)
        return Payment.objects.none()

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return api_response(data=serializer.data)
