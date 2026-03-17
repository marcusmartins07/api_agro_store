from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Produto, PrecoProduto, Categoria
from .serializers import ProdutoSerializer, PrecoProdutoSerializer, CategoriaSerializer


class CategoriaViewSet(viewsets.ModelViewSet):
    serializer_class = CategoriaSerializer

    def get_queryset(self):
        queryset = Categoria.objects.all()

        ativo = self.request.query_params.get("ativo")

        if ativo is not None:
            queryset = queryset.filter(ativo=ativo.lower() == "true")

        return queryset

class PrecoProdutoViewSet(viewsets.ModelViewSet):
    queryset = PrecoProduto.objects.all()
    serializer_class = PrecoProdutoSerializer


class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.select_related('categoria').prefetch_related('precos').all()
    serializer_class = ProdutoSerializer