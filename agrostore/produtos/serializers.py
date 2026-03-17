from rest_framework import serializers
from .models import Produto, PrecoProduto, Categoria


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = (
            'categoria_id',
            'nome',
            'ativo'
        )


class ProdutoSerializer(serializers.ModelSerializer):
    categoria_nome = serializers.StringRelatedField(source='categoria') 
    categoria = serializers.PrimaryKeyRelatedField(                     
        queryset=Categoria.objects.all()
    )
    preco = serializers.SerializerMethodField()
    preco_original = serializers.SerializerMethodField()
    desconto = serializers.SerializerMethodField()

    class Meta:
        model = Produto
        fields = [
            'produto_id',
            'nome',
            'categoria',
            'categoria_nome',  
            'preco',
            'preco_original',
            'desconto',
            'estoque',
        ]

    def get_preco_atual(self, obj):
        return obj.precos.filter(vigencia_fim__isnull=True).last()

    def get_preco(self, obj):
        preco = self.get_preco_atual(obj)
        if preco:
            return preco.preco_desconto or preco.preco_venda
        return None

    def get_preco_original(self, obj):
        preco = self.get_preco_atual(obj)
        if preco:
            return preco.preco_venda
        return None

    def get_desconto(self, obj):
        preco = self.get_preco_atual(obj)
        if preco:
            return preco.porcentagem_desconto
        return None

class PrecoProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrecoProduto
        fields = [
            'id',
            'produto',
            'preco_venda',
            'preco_custo',
            'preco_desconto',
            'porcentagem_desconto',
            'vigencia_inicio',
            'vigencia_fim',
        ]
        read_only_fields = ['preco_desconto', 'porcentagem_desconto', 'vigencia_fim']