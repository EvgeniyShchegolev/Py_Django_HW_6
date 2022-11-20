from rest_framework import serializers
from .models import Stock, StockProduct, Product


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):

    class Meta:
        model = StockProduct
        fields = ['id', 'product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions']

    def create(self, validated_data):

        positions = validated_data.pop('positions')

        stock = super().create(validated_data)

        for position in positions:
            StockProduct.objects.create(stock=stock, **position)

        return stock

    def update(self, instance, validated_data):

        positions = validated_data.pop('positions')
        for position in positions:
            print(position)

        stock = super().update(instance, validated_data)

        for position in positions:
            obj, created = StockProduct.objects.update_or_create(
                stock=stock,
                product=position['product'],
                defaults={'stock': stock, 'product': position['product'],
                          'quantity': position['quantity'], 'price': position['price']}
            )

        return stock
