from rest_framework import viewsets, permissions
from .models import Loja
from .serializers import LojaSerializer


class LojaViewSet(viewsets.ModelViewSet):
    queryset = Loja.objects.select_related('proprietario').all()
    serializer_class = LojaSerializer
    http_method_names = ['get', 'post', 'patch']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(proprietario=self.request.user)