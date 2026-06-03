from rest_framework import status, generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from core.utils import api_response
from .serializers import RegisterSerializer, CustomTokenObtainPairSerializer, UserSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            error_msg = "Invalid credentials or pending approval."
            if hasattr(e, 'detail') and isinstance(e.detail, (dict, list)):
                if isinstance(e.detail, list):
                    error_msg = str(e.detail[0])
                elif 'non_field_errors' in e.detail:
                    error_msg = str(e.detail['non_field_errors'][0])
                else:
                    error_msg = str(e.detail)
            return api_response(success=False, error=error_msg, status=status.HTTP_401_UNAUTHORIZED)
        
        return api_response(data=serializer.validated_data)



class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response(data=serializer.data, status=status.HTTP_201_CREATED)
        return api_response(success=False, error=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return api_response(data=serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(self.get_object(), data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return api_response(data=serializer.data)
        return api_response(success=False, error=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
