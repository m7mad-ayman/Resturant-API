from rest_framework.generics import  RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAdminUser
from rest_framework.decorators import permission_classes ,api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from .permissions import *
from decimal import Decimal

@api_view(["GET","POST","PUT","DELETE"])
@permission_classes([AllowAny])
def menuView(request,**kwargs):
    if request.method == "GET":
        if "id" in kwargs:
            item = MenuItem.objects.get(id=id)
            serial = MenuSerializer(menu)
            return Response(serial.data,status=status.HTTP_200_OK)
        else:
            menu = MenuItem.objects.all()
            serial = MenuSerializer(menu,many=True)
            return Response(serial.data,status=status.HTTP_200_OK)
    
    elif request.method == "POST":
        if request.user.is_authenticated and request.user.is_superuser:
            item = MenuItem.objects.create()
            errors = {}
            if not request.data.get("name") :
                errors['name'] = ["This field is required."]
            if not request.data.get("description") :
                errors['description'] = ["This field is required."]
            if not request.data.get("price") :
                errors['price'] = ["This field is required."]
            if not request.data.get('ingredients'):
                errors['ingredients'] = ["This field is required. 'ingredients':[{'name':'value','amount':value}]"]
            if not request.data.get('category'):
                errors['category'] = ["This field is required."]
            if errors:
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)
            if MenuItem.objects.filter(name=request.data.get("name")).exists():
                return Response({"message":"This Menu item already exist , please choose unique name"}, status=status.HTTP_400_BAD_REQUEST)
            item.name= request.data.get("name")
            item.description = request.data.get("description")
            item.price = request.data.get("price")
            ingredients = request.data.get('ingredients')
            
            if request.data.get('is_available'):
                item.is_available = request.data.get('is_available')
            
            item.category = Category.objects.get(name=request.data.get('category'))
            for ingredient in ingredients:
                saved = Ingredient.objects.get(name = ingredient.get('name'))
                item.ingredients.add(saved)
                IngerdientItem.objects.create(ingredient=saved,menuitem = item,amount=Decimal(ingredient.get('amount')))
            item.save()
            serial=MenuSerializer(item)
            return Response(serial.data,status=status.HTTP_201_CREATED)
        else:
            return Response({"message":"You have no permission"}, status=status.HTTP_200_OK)
        
    elif request.method == "PUT":
        if request.user.is_staff :
            if "id" in kwargs:
                try:
                    item = MenuItem.objects.get(id=id)
                except MenuItem.DoesNotExist:
                    return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

                serializer = MenuSerializer(MenuItem, data=request.data, partial=True) 
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': 'You should specifie item with [id]'})
            
    elif request.method == "DELETE":
        if request.user.is_superuser:
            if "id" in kwargs:
                try:
                    item = MenuItem.objects.get(id=id)
                except MenuItem.DoesNotExist:
                    return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

                item.delete()
                return Response({'message': 'Product deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'message': 'You should specifie item with [id]'})



@permission_classes([IsSuperUser])
class IngredientsView(RetrieveUpdateDestroyAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    def get(self, request, *args, **kwargs):
        if 'id' in kwargs:
            return super().get(request, *args, **kwargs)
        else:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET","PUT","DELETE"])
@permission_classes([IsAdminUser])
def tableNumView(request,num):
    try:
       table = Table.objects.get(number=num)
    except Exception as error:
        return Response({"error":str(error)},status=status.HTTP_400_BAD_REQUEST)
    if request.method == "GET":
        serial = TableSerializer(table)
        return Response(serial.data,status=status.HTTP_200_OK)
        
    elif request.method == "PUT":
        serializer = TableSerializer(table,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "DELETE":
        table.delete()
        return Response({'message': 'Table deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

@api_view(["GET","POST"])
@permission_classes([IsAdminUser])
def tableView(request):
    if request.method == "GET":
        table = Table.objects.all()
        serial = TableSerializer(table,many=True)
        return Response(serial.data,status=status.HTTP_200_OK)
    
    elif request.method == "POST":
        if request.user.is_superuser:
            serial = TableSerializer(data=request.data)
            if serial.is_valid():
                serial.save()
                return Response(serial.data,status=status.HTTP_201_CREATED)
            return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":"You have no permission"})

@api_view(["GET","POST"])
@permission_classes([IsAuthenticated])
def reservationView(request):
    if request.method == "GET":
        if request.user.is_staff:

            reservations = Reservation.objects.all()
            serial = TableSerializer(reservations,many=True)
            return Response(serial.data,status=status.HTTP_200_OK)
        else:
            return Response({"message":"You have no permission"})
        
    
    elif request.method == "POST":
            reservation =Reservation()
            errors = {}
            if not request.data.get("name") :
                errors['name'] = ["This field is required."]
            if not request.data.get("people") :
                errors['people'] = ["This field is required."]
            if not request.data.get("date") :
                errors['date'] = ["This field is required."]
            if errors:
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)

            reservation.customer_name = request.data.get("name")
            tables = Table.objects.filter(capacity__gte=request.data.get("people"))
            chosed = None
            if tables.exists():
                for table in tables:
                    if not Reservation.objects.filter(reservation_date = request.data.get("date"),table=table).exists():
                        chosed = table
                        break
            if chosed == None:
                return Response({"message":"Unfortunately our restaurant is full on this day, or this capacity is not valid"})
            reservation.reservation_date = request.data.get("date")
            reservation.table=chosed
            reservation.guests_num = request.data.get("people")
            if request.data.get("status"):
                reservation.status=request.data.get("status")
            reservation.save()
            serial = ReservationSerializer(reservation)
            return Response(serial.data,status=status.HTTP_201_CREATED)

@api_view(["GET","PUT","DELETE"])
@permission_classes([IsAuthenticated])
def reservationIdView(request,id):
    try:
       reservation = Reservation.objects.get(id=id)
    except Exception as error:
        return Response({"error":str(error)},status=status.HTTP_400_BAD_REQUEST)
    if request.method == "GET":
        serial = ReservationSerializer(reservation)
        return Response(serial.data,status=status.HTTP_200_OK)
    
    elif request.method == "PUT":
        if request.user.is_staff:
            errors={}
            if not request.data.get("name") :
                errors['name'] = ["This field is required."]
            if not request.data.get("people") :
                errors['people'] = ["This field is required."]
            if not request.data.get("date") :
                errors['date'] = ["This field is required."]
            if errors:
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)
            reservation.customer_name = request.data.get("name")
            if request.data.get("status"):
                reservation.status=request.data.get("status")
            if request.data.get("date"):
                tables = Table.objects.filter(capacity__gte=reservation.guests_num)
                chosed = None
                if tables.exists():
                    for table in tables:
                        if not Reservation.objects.filter(reservation_date = request.data.get("date"),table=table).exists():
                            chosed = table
                            break
            
                if chosed == None:
                    return Response({"message":"Sorry no tables available in this date"})
                reservation.table=chosed
                reservation.reservation_date=request.data.get("date")
            reservation.save()
            serial= ReservationSerializer(reservation)
            return Response(serial.data,status=status.HTTP_202_ACCEPTED)
        else:
            return Response({"message":"You have no permission"})
    
    elif request.method == "DELETE":
        if request.user.is_superuser:
            reservation.delete()
            return Response({'message': 'Reservation deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message":"You have no permission"})


@api_view(["POST","GET"])
@permission_classes([IsAuthenticated])
def orderView(request):
    if request.method == "POST":
            order = Order.objects.create()
            name= request.data.get('name')
            order_type =request.data.get('type')
            errors = {}
            if not name :
                errors['name'] = ["This field is required."]
            if not order_type :
                errors['type'] = ["This field is required."]
            order.customer_name = name
            order.order_type = order_type
            if order.order_type == "dine-in":
                if not request.data.get("table_number"):
                    errors['table_number'] = ["This field is required, while its dine-in order"]
                order.table = Table.objects.get(number=request.data.get("table_number"))
            if not order.order_type == "delivery":
                order.delivery = 0
            items =request.data.get('items')
            if not items:
                errors['items'] = ["This field is required."]
            if errors:
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)
            alert={}
            total_price =0
            for item in items:
                menuitem = MenuItem.objects.get(name=item.get('name'))
                OrderItem.objects.create(menuitem=menuitem,order=order,quantity=item.get('quantity'))
                order.order_items.add(menuitem)
                ingredients = IngerdientItem.objects.filter(menuitem=menuitem)
                for relation in ingredients:
                    ingredient=relation.ingredient
                    ingredient.quantity -= item.get("quantity")*relation.amount
                    ingredient.save()
                    if ingredient.quantity <= ingredient.threshold:
                        alert[ingredient.name]=["this ingredient is about to run out"]

                total_price += item.get('quantity')*menuitem.price
            order.total_price = total_price + order.delivery
            order.save()
            serial = OrderSerializer(order)
            if alert:
                result = serial.data
                result["alert"]=alert
                return Response(result,status=status.HTTP_201_CREATED)
            return Response(serial.data,status=status.HTTP_201_CREATED)
    
    
    elif request.method == "GET":
        if request.user.is_staff:
            orders = Order.objects.all()
            serial = OrderSerializer(orders,many=True)
            return Response(serial.data,status=status.HTTP_200_OK)
        else:
            return Response({"message":"You have no permission"})
        
@api_view(["PUt","GET","DELETE"])
@permission_classes([IsAuthenticated])        
def orderIdView(request,id):
    try:
       order = Order.objects.get(id=id)
    except Exception as error:
        return Response({"error":str(error)},status=status.HTTP_400_BAD_REQUEST)
    if request.method == "GET":
        serial = OrderSerializer(order)
        return Response(serial.data,status=status.HTTP_200_OK)
    
    elif request.method == "PUT":
        if request.user.is_staff :
            errors = {}
            if not request.data.get("name") :
                errors['name'] = ["This field is required."]
            if not request.data.get("type") :
                errors['type'] = ["This field is required."]
            if not request.data.get('items'):
                errors['items'] = ["This field is required."]
            if errors:
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)
            
            items =OrderItem.objects.filter(order=order)

            alert={}
            for item in items:
                menuitem = item.menuitem
                order.order_items.remove(menuitem)
                ingredients = IngerdientItem.objects.filter(menuitem=menuitem)
                for relation in ingredients:
                    ingredient=relation.ingredient
                    ingredient.quantity += item.quantity*relation.amount
                    ingredient.save()
                    if ingredient.quantity <= ingredient.threshold:
                        alert[ingredient.name]=["this ingredient is about to run out"]
                item.delete()
            order.customer_name = request.data.get("name")
            order.order_type = request.data.get('type')
            if order.order_type == "dine-in":
                if not request.data.get("table_number"):
                    errors['table_number'] = ["This field is required, while its dine-in order"]
                order.table = Table.objects.get(number=request.data.get("table_number"))
            items =request.data.get("items")
            if not items:
                errors['items'] = ["This field is required."]
            if errors:
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)
            alert={}
            total_price =0
            for item in items:
                menuitem = MenuItem.objects.get(name=item.get('name'))
                OrderItem.objects.create(menuitem=menuitem,order=order,quantity=item.get('quantity'))
                order.order_items.add(menuitem)
                ingredients = IngerdientItem.objects.filter(menuitem=menuitem)
                for relation in ingredients:
                    ingredient=relation.ingredient
                    ingredient.quantity -= item.get("quantity")*relation.amount
                    ingredient.save()
                    if ingredient.quantity <= ingredient.threshold:
                        alert[ingredient.name]=["this ingredient is about to run out"]

                total_price += item.get('quantity')*menuitem.price
            order.total_price = total_price + order.delivery
            order.save()
            serial = OrderSerializer(order)
            if alert:
                result = serial.data
                result["alert"]=alert
                return Response(result,status=status.HTTP_201_CREATED)
            return Response(serial.data,status=status.HTTP_201_CREATED)
        else:
            return Response({"message":"You have no permission"})
    

    elif request.method == "DELETE":
        if request.user.is_superuser:
            order.delete()
            return Response({'message': 'Order deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message":"You have no permission"})