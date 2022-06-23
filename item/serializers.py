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
    category = serializers.SerializerMethodField()
    
    def get_category(self, obj):
        return obj.category.name
    
    class Meta:
        model = Item
        fields = ["name", "category", "image_url"]
        
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["delivery_address", "order_date"]
        
class ItemOrderSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)
    item = ItemSerializer(read_only=True)
    class Meta:
        model = ItemOrder
        fields = ["id", "order", "item", "item_count"]