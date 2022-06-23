from rest_framework import serializers

from .models import Category 
from .models import Item
from .models import Order
from .models import ItemOrder

class CategorySeriralizer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name"]
        
class ItemSerializer(serializers.ModelSerializer):
    category = CategorySeriralizer(many=True, read_only=True)
    class Meta:
        model = Item
        fields = ["name", "category", "img_url"]
        
class OrderSerializer(serializers.ModelSerializer):
    item = ItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ["delivery_address", "order", "item"]
        
class ItemOrderSerializer(serializers.ModelSerializer):
    order = OrderSerializer(many=True)
    item = ItemSerializer(many=True)
    class Meta:
        model = ItemOrder
        fields = ["order", "item", "item_count"]