from rest_framework import viewsets, permissions, status
from .models import CustomUser, Empresa, Producto, Categoria, Cliente, Orden,Inventario
from .serializers import CustomUserSerializer, AuthTokenSerializer, EmpresaSerializer, ProductoSerializer, CategoriaSerializer, ClienteSerializer, OrdenSerializer, InventarioSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.views import ObtainAuthToken
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff

class IsExternalUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and not request.user.is_staff

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create']:
            return [permissions.AllowAny()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        else:
            return [IsAuthenticated()]

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        user_data = {
            "username": user.username,
            "admin": user.is_staff
        }

        return Response({
            'token': token.key,
            'user_id': user.pk,
            'user': user_data
        })
        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    user = request.user 
    serializer = CustomUserSerializer(user) 
    token, created = Token.objects.get_or_create(user=user)

    user_data = {
        "username": user.username,
        "admin": user.is_staff
    }

    return Response({
        'token': token.key,
        'user_id': user.pk,
        'user': user_data
    })
    return Response(serializer.data)
  
class CustomLogoutView(APIView):
    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({'detail': 'Cierre de sesión exitoso.'}, status=status.HTTP_200_OK)

class EmpresaViewSet(viewsets.ModelViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated | IsAdminUser]
   
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        else:
            return [IsAuthenticated()]
        
    def get_queryset(self):
        user = self.request.user

        if not user.is_staff:
            return Empresa.objects.all()
        
        user_empresa = get_object_or_404(Empresa, user=user)
        return Empresa.objects.filter(pk=user_empresa.pk)

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated | IsAdminUser]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        else:
            return [IsAuthenticated()]
        
    def list_by_empresa(self, request, empresa_id=None):
        try:
            empresa_id = int(empresa_id)
            productos = Producto.objects.filter(empresa=empresa_id)
            serializer = self.get_serializer(productos, many=True)
            return Response(serializer.data)
        except ValueError:
            return Response({"error": "Invalid empresa_id"}, status=400)

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated | IsAdminUser]
    

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated | IsAdminUser]

class OrdenViewSet(viewsets.ModelViewSet):
    queryset = Orden.objects.all()
    serializer_class = OrdenSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated | IsAdminUser]
    
    
class InventarioViewSet(viewsets.ModelViewSet):
    queryset = Inventario.objects.all()
    serializer_class = InventarioSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated | IsAdminUser]
   
    def get_permissions(self):
        if self.action in ['create']:
            return [IsAdminUser()]
        else:
            return [IsAuthenticated()]

    

# Repite este proceso para los otros modelos (Categoría, Cliente, Orden)
