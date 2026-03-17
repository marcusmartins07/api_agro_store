from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/usuarios/', include('agrostore.usuarios.urls')),
    path('api/v1/produtos/', include('agrostore.produtos.urls')),
]