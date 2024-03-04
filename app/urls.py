from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from .views import CustomUserViewSet, CustomAuthToken, get_user_info, CustomLogoutView, EmpresaViewSet, ProductoViewSet, CategoriaViewSet, ClienteViewSet, OrdenViewSet

router = DefaultRouter()
router.register(r'users', CustomUserViewSet)
router.register(r'empresas', EmpresaViewSet, basename='empresa')
router.register(r'productos', ProductoViewSet)
router.register(r'categorias', CategoriaViewSet)
router.register(r'clientes', ClienteViewSet)
router.register(r'ordenes', OrdenViewSet)

urlpatterns = [
    path('user', get_user_info, name='user'),
    path('login', CustomAuthToken.as_view(), name='login'),
    path('logout', CustomLogoutView.as_view(), name='logout'),
    path('productos/empresa/<int:empresa_id>', ProductoViewSet.as_view({'get': 'list_by_empresa'}), name='producto-list-by-empresa'),
    path('', include(router.urls)),
]
