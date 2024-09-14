from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.http import JsonResponse
from .models import *

class CategorySerializer(ModelSerializer):
    class Meta:
        model =Category
        fields =["name"]

class TableSerializer(ModelSerializer):
    class Meta:
        model = Table
        fields = '__all__'

class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'

class IngredientItemSerializer(ModelSerializer):
    ingredient = serializers.StringRelatedField()
    class Meta:
        model = IngerdientItem
        fields = ["ingredient","amount"]

class MenuSerializer(ModelSerializer):
    ingredients =serializers.SerializerMethodField('get_ingredients')
    category = serializers.StringRelatedField()
    class Meta:
        model = MenuItem
        fields = ['name','description','price','is_available','ingredients','category']
    def get_ingredients(self,obj):
        items = IngerdientItem.objects.filter(menuitem= MenuItem.objects.get(name=obj.name))
        serial = IngredientItemSerializer(items,many=True)
        return serial.data

class OrderItemSerializer(ModelSerializer):
    menuitem = serializers.StringRelatedField()
    class Meta:
        model = OrderItem
        fields = ['menuitem','quantity']

class OrderSerializer(ModelSerializer):
    items =serializers.SerializerMethodField('get_items')
    class Meta:
        model = Order
        fields = ['id','customer_name','items','order_type','delivery','table','total_price','status','created_at']
    def get_items(self, obj):
        # do all things needed here.
       items =OrderItem.objects.filter(order=Order.objects.get(id=obj.id))
       serializer = OrderItemSerializer(items,many=True)
       return serializer.data
     
    
class ReservationSerializer(ModelSerializer):
    table = serializers.StringRelatedField()
    class Meta:
        model = Reservation
        fields = '__all__'